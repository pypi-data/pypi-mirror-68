import logging
import time

from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint
from scrapy_redis.BloomDemo import BloomFilter
from . import defaults
from .connection import get_redis_from_settings
from scrapy.utils.project import get_project_settings


logger = logging.getLogger(__name__)


class RFPDupeFilter(BaseDupeFilter):
    count = 0
    """Redis-based request duplicates filter.

    This class can also be used with default Scrapy's scheduler.

    """

    logger = logger

    def __init__(self, server, key, use_bloom =  False, bit = 30, hash_number=6,debug=False):
        """Initialize the duplicates filter.

        Parameters
        ----------
        server : redis.StrictRedis
            The redis server instance.
        key : str
            Redis key Where to store fingerprints.
        debug : bool, optional
            Whether to log filtered requests.

        """
        settings = get_project_settings()
        self.use_bloom = settings.getbool('USE_BLOOM')
        self.server = server
        self.key = key + str(time.time())
        self.debug = debug
        self.logdupes = True
        self.bit = settings.getint('BLOOMFILTER_BIT')
        self.hash_number = settings.getint('BLOOMFILTER_HASH_NUMBER')
        self.bf = BloomFilter(server,self.key,bit,hash_number)

    @classmethod
    def from_settings(cls, settings):
        """Returns an instance from given settings.

        This uses by default the key ``dupefilter:<timestamp>``. When using the
        ``scrapy_redis.scheduler.Scheduler`` class, this method is not used as
        it needs to pass the spider name in the key.

        Parameters
        ----------
        settings : scrapy.settings.Settings

        Returns
        -------
        RFPDupeFilter
            A RFPDupeFilter instance.


        """
        settings = get_project_settings()
        # use_bloom = settings.getbool('USE_BLOOM')
        server = get_redis_from_settings(settings)
        # XXX: This creates one-time key. needed to support to use this
        # class as standalone dupefilter with scrapy's default scheduler
        # if scrapy passes spider on open() method this wouldn't be needed
        # TODO: Use SCRAPY_JOB env as default and fallback to timestamp.
        key = defaults.DUPEFILTER_KEY % {'timestamp': int(time.time())}
        # key = defaults.DUPEFILTER_KEY + str(int(time.time()))
        debug = settings.getbool('DUPEFILTER_DEBUG')
        bit = settings['BLOOMFILTER_BIT']
        hash_number = settings['BLOOMFILTER_HASH_NUMBER']
        return cls(server, key=key, debug=debug, bit=bit, hash_number=hash_number)

    @classmethod
    def from_crawler(cls, crawler):
        """Returns instance from crawler.

        Parameters
        ----------
        crawler : scrapy.crawler.Crawler

        Returns
        -------
        RFPDupeFilter
            Instance of RFPDupeFilter.

        """
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        """Returns True if request was already seen.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        bool

        """
        fp = self.request_fingerprint(request)

        if self.use_bloom == True:
            if self.bf.exist(fp):
                RFPDupeFilter.count += 1
                print('重复数量', RFPDupeFilter.count)
                return True
            self.bf.put_into(fp)
            return False
        else:
            added = self.server.sadd(self.key+'_set', fp)
            return added == 0

    def request_fingerprint(self, request):
        """Returns a fingerprint for a given request.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        str

        """
        return request_fingerprint(request)

    def close(self, reason=''):
        """Delete data on close. Called by Scrapy's scheduler.

        Parameters
        ----------
        reason : str, optional

        """
        self.clear()

    def clear(self):
        """Clears fingerprints data."""
        self.server.delete(self.key)

    def log(self, request, spider):
        """Logs given request.

        Parameters
        ----------
        request : scrapy.http.Request
        spider : scrapy.spiders.Spider

        """
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False

