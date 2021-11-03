from notion_py.applications.prop_matcher.common.base import Matcher


class MatchertoItself(Matcher):
    def execute(self):
        for pagelist in [self.bs.dates,
                         self.bs.journals, self.bs.memos, self.bs.writings]:
            for dom in pagelist:
                if dom.props.read_at('to_itself'):
                    continue
                dom.props.write_at('to_itself', [dom.block_id])
