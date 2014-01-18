from drape.render import render

class WidgetBase(object):
    def __str__(self):
        return self.run()

class Pager(WidgetBase):
    def __init__(self, per_page, current_page, total_count, page_width=5):
        self.__per_page = per_page
        self.__current_page = current_page
        self.__total_count = total_count
        self.__page_width = page_width

    def run(self):
        page_count = (self.__total_count + self.__per_page - 1) / self.__per_page

        page_begin = self.__current_page - self.__page_width / 2
        page_end = page_begin + self.__page_width
        if page_begin < 1:
            page_begin = 1
            page_end = min(self.__page_width, page_count - 2) + 1
        elif page_end >= page_count:
            page_end = page_count - 1
            page_begin = max(1, page_end - self.__page_width)

        return render(
            'widget/Pager',
            {
                'page_count': page_count,
                'current_page': self.__current_page,
                'total_count': self.__total_count,
                'page_begin': page_begin,
                'page_end': page_end
            }
        )
