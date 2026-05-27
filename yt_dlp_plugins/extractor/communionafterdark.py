# ⚠ Don't use relative imports
from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import (
    ExtractorError,
    parse_duration,
    unified_strdate,
)


class CommunionAfterDarkIE(InfoExtractor):
    IE_NAME = 'communionafterdark'
    IE_DESC = 'Communion After Dark'
    _VALID_URL = r'https?://(?:www\.)?communionafterdark\.com/(?P<id>[^/?#]+)'

    _TESTS = [{
        'url': 'https://www.communionafterdark.com/episode',
        'only_matching': True,
    }]

    def _real_extract(self, url):
        display_id = self._match_id(url)
        webpage = self._download_webpage(url, display_id)

        title = (
            self._html_search_meta(['og:title', 'twitter:title'], webpage, default=None)
            or self._html_search_regex(r'<title>([^<]+)</title>', webpage, 'title', default=None)
            or display_id)

        description = self._html_search_meta(
            ['og:description', 'description'], webpage, default=None)

        thumbnail = self._html_search_meta(
            ['og:image', 'twitter:image'], webpage, default=None)

        # Look for audio/video sources embedded in the page
        # Try HTML5 <audio> or <video> source tags
        formats = []
        audio_url = self._search_regex(
            [
                r'<audio[^>]+src=["\']([^"\']+)["\']',
                r'<source[^>]+src=["\']([^"\']+\.mp3)["\']',
                r'<source[^>]+src=["\']([^"\']+\.m4a)["\']',
                r'<source[^>]+src=["\']([^"\']+\.ogg)["\']',
            ],
            webpage, 'audio URL', default=None)

        if audio_url:
            formats.append({
                'url': audio_url,
                'vcodec': 'none',
            })

        if not formats:
            # Fall back to generic embedded player detection
            raise ExtractorError('No media found on this page', expected=True)

        return {
            'id': display_id,
            'title': title,
            'description': description,
            'thumbnail': thumbnail,
            'formats': formats,
        }
