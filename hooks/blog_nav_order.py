"""把博客侧栏里“归档”和“分类”两个分区的上下顺序对调。

mkdocs-material 的 blog 插件在构建导航时，固定按“归档 -> 分类”的顺序把这两个
分区附加到博客索引页所在的分区下面，插件本身没有提供顺序配置项。这里在该事件
之后运行（event_priority -60，晚于 blog 插件的 -50），把两者对调。

如果 blog 插件日后的行为变化导致匹配不到，此钩子不会报错，只是不生效。
"""

from mkdocs.plugins import event_priority
from mkdocs.structure.nav import Section

# 取自 mkdocs-material 语言包里的 blog.archive / blog.categories
ARCHIVE_TITLES = {"归档", "Archive"}
CATEGORIES_TITLES = {"分类", "Categories"}


def _sections(items):
    """深度优先遍历导航树，产出所有分区（Section）。"""
    for item in items:
        if isinstance(item, Section):
            yield item
            yield from _sections(item.children)


@event_priority(-60)
def on_nav(nav, *, config, files):
    for section in _sections(nav.items):
        children = section.children
        for index in range(len(children) - 1):
            first, second = children[index], children[index + 1]
            if (
                isinstance(first, Section)
                and isinstance(second, Section)
                and first.title in ARCHIVE_TITLES
                and second.title in CATEGORIES_TITLES
            ):
                children[index], children[index + 1] = second, first
    return nav
