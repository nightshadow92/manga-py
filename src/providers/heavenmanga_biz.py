from src.provider import Provider
from .helpers.std import Std


class HeavenMangaBiz(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-', 2)
        return self.normal_arc_name(idx)

    def get_chapter_index(self) -> str:
        return self.re.search(r'-chap-(\d+)', self.chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/{}/')

    def get_manga_name(self) -> str:
        s = self.domain[self.domain.rfind('.'):]
        selector = r'\%s/([^/]+)'
        if ~self.get_url().find('-chap-'):
            selector += '-chap-'
        return self._get_name(selector % s)

    def get_chapters(self):
        selector = '.chapters-wrapper h2.chap > a'
        pages = self._elements('a.next.page-numbers')
        items = self._elements(selector)
        if pages:
            pages = self.re.search(r'/page-(\d+)', pages[-1].get('href')).group(1)
            for i in range(1, int(pages)):
                url = '{}/{}/page-{}'.format(self.domain, self.manga_name, i + 1)
                items += self._elements(selector, self.http_get(url))
        return items

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '.chapter-content img')

    def get_cover(self) -> str:
        return self._cover_from_content('.comic-info .thumb > img')


main = HeavenMangaBiz
