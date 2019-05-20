from app.parser.tmListener import tmListener


class tmParseListener(tmListener):

    def __init__(self, tm):
        self.tm = tm
        self.titledict = {
            "rwRt": "R",
            "rRt": "R",
            "rRl": "R",
            "rwLt": "L",
            "rLt": "L",
            "rLl": "L"
        }

    def parselist(self, ctx, list):
        x = ctx.children[3]
        for i in x.children:
            if str(i) == ',':
                continue
            else:
                list.append(str(i.children[0]))

    def enterStates(self, ctx):
        self.parselist(ctx, self.tm.states)

    def enterStart(self, ctx):
        self.tm.start.append(str(ctx.children[3]))

    def enterAccept(self, ctx):
        self.parselist(ctx, self.tm.accept)

    def enterReject(self, ctx):
        self.parselist(ctx, self.tm.reject)

    def enterAlpha(self, ctx):
        self.parselist(ctx, self.tm.alpha)

    def enterTalpha(self, ctx):
        self.parselist(ctx, self.tm.talpha)

    def enterTransfunc(self, ctx):
        tmp = []
        x = ctx.children[0]
        title = str(x.children[0])
        tmp.append(self.titledict[title])
        tmp.append(str(x.children[1].children[0]))
        tmp.append(str(x.children[2].children[0]))
        if len(x.children) == 5:
            tmp.append(str(x.children[3].children[0]))
        if len(x.children) == 6:
            tmp.append(str(x.children[4].children[0]))
            tmp.append(str(x.children[3].children[0]))
        self.tm.trans.append(tmp)
