from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    keyword: str
    source_url: str
    note: str
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None
    rating: int = 0

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.rating = max(0, min(5, self.rating))

    def format_brief(self) -> str:
        tag_str = ", ".join(self.tags) if self.tags else "无标签"
        return f"[{self.keyword}] ({self.source_url}) - {self.note[:30]}... 标签: {tag_str} 评分: {self.rating}/5"

    def format_detailed(self) -> str:
        return (
            f"关键词: {self.keyword}\n"
            f"来源: {self.source_url}\n"
            f"笔记: {self.note}\n"
            f"标签: {', '.join(self.tags) if self.tags else '无'}\n"
            f"创建时间: {self.created_at}\n"
            f"评分: {'★' * self.rating}{'☆' * (5 - self.rating)}\n"
        )


@dataclass
class KeywordNoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def list_all_brief(self) -> List[str]:
        return [note.format_brief() for note in self.notes]

    def list_all_detailed(self) -> List[str]:
        return [note.format_detailed() for note in self.notes]

    def top_rated(self, top_n: int = 3) -> List[KeywordNote]:
        sorted_notes = sorted(self.notes, key=lambda n: n.rating, reverse=True)
        return sorted_notes[:top_n]


def format_collection_summary(collection: KeywordNoteCollection) -> str:
    lines = ["===== 关键词笔记汇总 ====="]
    lines.append(f"笔记总数: {len(collection.notes)}")
    if collection.notes:
        top = collection.top_rated(3)
        lines.append("评分最高笔记:")
        for i, note in enumerate(top, 1):
            lines.append(f"  {i}. {note.keyword} (评分: {note.rating})")
        lines.append("所有笔记简要:")
        for brief in collection.list_all_brief():
            lines.append(f"  - {brief}")
    lines.append("=========================")
    return "\n".join(lines)


def demo_usage() -> None:
    collection = KeywordNoteCollection()

    note1 = KeywordNote(
        keyword="乐鱼体育",
        source_url="https://leyuindex.com.cn",
        note="乐鱼体育是一个综合性体育赛事平台，提供多种体育项目的资讯和数据服务。",
        tags=["体育", "平台", "数据"],
        rating=4,
    )
    collection.add_note(note1)

    note2 = KeywordNote(
        keyword="乐鱼体育APP",
        source_url="https://leyuindex.com.cn/app",
        note="乐鱼体育移动端应用，支持iOS和Android系统，方便用户随时随地获取体育信息。",
        tags=["移动端", "应用", "体育"],
        rating=5,
    )
    collection.add_note(note2)

    note3 = KeywordNote(
        keyword="乐鱼体育赛事",
        source_url="https://leyuindex.com.cn/events",
        note="涵盖足球、篮球、网球等多种热门赛事的实时比分和赛程安排。",
        tags=["赛事", "足球", "篮球"],
        rating=3,
    )
    collection.add_note(note3)

    print("详细输出示例1:")
    print(note1.format_detailed())
    print("-" * 40)

    print("详细输出示例2:")
    print(note2.format_detailed())
    print("-" * 40)

    print("汇总信息:")
    print(format_collection_summary(collection))

    print("\n搜索 '乐鱼':")
    for result in collection.find_by_keyword("乐鱼"):
        print(result.format_brief())

    print("\n标签 '体育' 的笔记:")
    for result in collection.find_by_tag("体育"):
        print(result.format_brief())


if __name__ == "__main__":
    demo_usage()