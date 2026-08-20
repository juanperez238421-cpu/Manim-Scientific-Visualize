from manim import *
import numpy as np
config.pixel_width=1920; config.pixel_height=1080; config.frame_width=16; config.frame_height=9; config.frame_rate=30; config.background_color=WHITE
INK=BLACK; GRAY="#D7D7D7"; PAPER="#F7F7F7"; RQ=.65; RN=.95; RS=1.25; WR=1.5; WE=2.2; WW=2.9
DATA=np.array([72,85,90,66,78,88])

def check():
    assert DATA.tolist()==[72,85,90,66,78,88]
    assert DATA.shape==(6,) and DATA[0]==72 and DATA[-1]==88
    assert DATA[1:4].tolist()==[85,90,66]
    assert DATA[DATA>=80].tolist()==[85,90,88]
    assert abs(DATA.mean()-79.83333333333333)<1e-10
    assert abs(DATA.std()-8.6874750199481)<1e-10
    assert abs(DATA.std(ddof=1)-9.516652072376433)<1e-10

class Statistics11ColabArrays(MovingCameraScene):
    def setup(self):
        super().setup(); check(); self.camera.background_color=WHITE; self.camera.frame.set(width=16); self.hg=None; self.sg=None
    def tx(self,s,n=28,b=False,mono=False):
        kw=dict(font_size=n,color=INK,weight=BOLD if b else NORMAL,line_spacing=.92)
        if mono: kw["font"]="DejaVu Sans Mono"
        return Text(s,**kw)
    def fit(self,m,w,h):
        if m.width>w:m.scale_to_fit_width(w)
        if m.height>h:m.scale_to_fit_height(h)
        return m
    def head(self,k,t,s):
        box=RoundedRectangle(width=.72,height=.52,corner_radius=.1,stroke_color=INK,fill_color=WHITE,fill_opacity=1)
        num=self.tx(f"{k:02d}",23,True).move_to(box); title=self.fit(self.tx(t,33,True),13.3,.58)
        row=VGroup(VGroup(box,num),title).arrange(RIGHT,buff=.24).to_edge(UP,buff=.16).to_edge(LEFT,buff=.48)
        rule=Line(LEFT*7.48,RIGHT*7.48,color=GRAY,stroke_width=2).next_to(row,DOWN,buff=.07)
        sub=self.fit(self.tx(s,20),14.2,.56).next_to(rule,DOWN,buff=.08).align_to(row,LEFT); nh=VGroup(row,rule)
        if self.hg is None:self.add(nh,sub)
        else:self.play(ReplacementTransform(self.hg,nh),ReplacementTransform(self.sg,sub),run_time=RQ)
        self.hg,self.sg=nh,sub
    def clear(self):
        keep=set()
        for g in (self.hg,self.sg):
            if g: keep|={id(x) for x in g.get_family()}
        gone=[m for m in self.mobjects if id(m) not in keep]
        if gone:self.play(*[FadeOut(m) for m in gone],run_time=RN)
    def panel(self,w,h,fill=PAPER):
        return RoundedRectangle(width=w,height=h,corner_radius=.12,stroke_color=INK,stroke_width=1.8,fill_color=fill,fill_opacity=1)
    def code(self,lines,w=6.8,title="COLAB CODE",size=23):
        body=VGroup(*[self.tx(x,size,False,True) for x in lines]).arrange(DOWN,aligned_edge=LEFT,buff=.18); self.fit(body,w-.55,4.5)
        cap=self.tx(title,22,True); content=VGroup(cap,body).arrange(DOWN,aligned_edge=LEFT,buff=.22); box=self.panel(w,max(1.25,content.height+.55))
        content.move_to(box).align_to(box,LEFT).shift(RIGHT*.28); return VGroup(box,content)
    def note(self,title,lines,w=5.7,size=22):
        body=VGroup(*[self.tx(x,size) for x in lines]).arrange(DOWN,aligned_edge=LEFT,buff=.15); content=VGroup(self.tx(title,25,True),body).arrange(DOWN,aligned_edge=LEFT,buff=.22); self.fit(content,w-.55,4.5)
        box=self.panel(w,max(1.2,content.height+.62),WHITE); content.move_to(box).align_to(box,LEFT).shift(RIGHT*.28); return VGroup(box,content)
    def strip(self,vals,w=1.18,h=.82,idx=True):
        cells=VGroup(); labels=VGroup()
        for i,v in enumerate(vals):
            r=Rectangle(width=w,height=h,stroke_color=INK,stroke_width=2,fill_color=WHITE,fill_opacity=1); cells.add(VGroup(r,self.tx(str(v),27,True).move_to(r)))
            if idx: labels.add(self.tx(str(i),19))
        cells.arrange(RIGHT,buff=0)
        if idx:
            for i,l in enumerate(labels):l.next_to(cells[i][0],DOWN,buff=.11)
            return VGroup(cells,labels)
        return VGroup(cells)
    def construct(self):
        self.opening(); self.meaning(); self.definition(); self.index(); self.slice(); self.twod(); self.stats(); self.filtering(); self.summary()
    def opening(self):
        g=VGroup(self.tx("GRADE 11 · STATISTICS · GOOGLE COLAB",27,True),self.tx("ARRAYS: DATA WITH POSITION AND STRUCTURE",47,True),Line(LEFT*6.4,RIGHT*6.4,color=GRAY),self.tx("Meaning · Definition · Index · Slicing · 2D arrays · Statistics",25),self.tx("Read the structure first. Then write the code.",23)).arrange(DOWN,buff=.28)
        self.fit(g,14,5.8); self.play(Write(g[0]),run_time=RN); self.play(Write(g[1]),run_time=RS); self.play(Create(g[2]),Write(g[3]),run_time=RN); self.play(FadeIn(g[4],shift=UP*.1),run_time=RN); self.wait(3.5); self.play(FadeOut(g),run_time=RN)
    def meaning(self):
        self.head(1,"WHAT DOES ARRAY MEAN?","An array is an ordered collection of values. Each position can be addressed by an index.")
        a=self.strip(DATA).move_to(LEFT*2.5+DOWN*.15); lab=self.tx("scores",25,True).next_to(a,LEFT,buff=.3)
        n=self.note("CORE IDEA",["Order matters.","Each value has a position.","Python indexing starts at 0.","Statistics stores datasets this way."],5.2,22).move_to(RIGHT*4.4+DOWN*.1)
        self.play(FadeIn(a[0],lag_ratio=.08),Write(lab),run_time=RS); self.play(FadeIn(a[1]),run_time=RN); self.wait(WR); self.play(FadeIn(n,shift=LEFT*.1),run_time=RN); self.wait(WW); self.clear()
    def definition(self):
        self.head(2,"HOW DO WE DEFINE ARRAYS IN COLAB?","A Python list and a NumPy ndarray look similar, but NumPy is built for numerical computation.")
        l=self.code(["scores_list = [72, 85, 90, 66, 78, 88]","type(scores_list)","# <class 'list'>"],6.9,"PYTHON LIST",21)
        r=self.code(["import numpy as np","scores = np.array([72, 85, 90, 66, 78, 88])","type(scores)","# <class 'numpy.ndarray'>"],6.9,"NUMPY ARRAY",21)
        VGroup(l,r).arrange(RIGHT,buff=.4).move_to(DOWN*.15); self.play(FadeIn(l),run_time=RN); self.wait(WR); self.play(FadeIn(r),run_time=RN)
        p=VGroup(self.tx("shape = (6,)",23,True,True),self.tx("dtype = int",23,True,True),self.tx("size = 6",23,True,True)).arrange(RIGHT,buff=.9).to_edge(DOWN,buff=.32)
        self.play(FadeIn(p,shift=UP*.1),run_time=RN); self.wait(WW); self.clear()
    def index(self):
        self.head(3,"INDEXING: ONE POSITION AT A TIME","Use square brackets after the array name. Negative indices count backward from the end.")
        a=self.strip(DATA).move_to(LEFT*2.6+DOWN*.1); c=self.code(["scores[0]   # 72","scores[2]   # 90","scores[-1]  # 88"],5.5,"READ A VALUE",25).move_to(RIGHT*4.3+DOWN*.1)
        self.play(FadeIn(a),FadeIn(c),run_time=RN); q=[SurroundingRectangle(a[0][i][0],buff=.05,color=INK,stroke_width=4) for i in (0,2,5)]
        syntax=self.tx("array[index]",27,True,True).to_edge(DOWN,buff=.35); self.play(Create(q[0]),Write(syntax),run_time=RN); self.wait(WR); self.play(ReplacementTransform(q[0],q[1]),run_time=RQ); self.wait(WR); self.play(ReplacementTransform(q[1],q[2]),run_time=RQ); self.wait(WE); self.clear()
    def slice(self):
        self.head(4,"SLICING: SELECT A RANGE","Pattern: start:stop:step. Start is included; stop is excluded.")
        a=self.strip(DATA).move_to(LEFT*2.5+UP*.25); c=self.code(["scores[1:4]","# array([85, 90, 66])","scores[::2]","# array([72, 90, 78])"],6.2,"EXAMPLES",23).move_to(RIGHT*4.2+DOWN*.55)
        syn=self.tx("scores[start : stop : step]",28,True,True).to_edge(DOWN,buff=.35); self.play(FadeIn(a),Write(syn),run_time=RN)
        hi=VGroup(*[SurroundingRectangle(a[0][i][0],buff=.04,color=INK,stroke_width=4) for i in (1,2,3)]); self.play(LaggedStart(*[Create(x) for x in hi],lag_ratio=.12),run_time=RN); self.play(FadeIn(c),run_time=RN); self.wait(WW); self.clear()
    def twod(self):
        self.head(5,"2D ARRAYS: ROWS AND COLUMNS","A table becomes a two-dimensional array. Its shape is (rows, columns).")
        vals=[[72,80,75],[85,88,91],[90,84,89],[66,70,74]]; rows=VGroup(*[self.strip(x,1.18,.74,False)[0] for x in vals]).arrange(DOWN,buff=0); box=SurroundingRectangle(rows,buff=.12,color=INK,stroke_width=2)
        g=VGroup(box,rows).move_to(LEFT*3.6+DOWN*.1); rl=VGroup(*[self.tx(f"row {i}",18) for i in range(4)]); cl=VGroup(*[self.tx(f"col {i}",18) for i in range(3)])
        for i,x in enumerate(rl):x.next_to(rows[i],LEFT,buff=.16)
        for i,x in enumerate(cl):x.next_to(rows[0][i],UP,buff=.17)
        g.add(rl,cl); c=self.code(["grades.shape   # (4, 3)","grades[1, 2]   # 91","grades[1, :]   # row 1","grades[:, 0]   # column 0"],6.4,"ROW, COLUMN",23).move_to(RIGHT*3.8+DOWN*.1)
        self.play(FadeIn(g),run_time=RN); self.wait(WR); self.play(FadeIn(c),run_time=RN); self.play(Create(SurroundingRectangle(rows[1][2][0],buff=.05,color=INK,stroke_width=4)),run_time=RN); self.wait(WE); self.clear()
    def stats(self):
        self.head(6,"WHY ARRAYS MATTER IN STATISTICS","NumPy applies calculations to the dataset directly and consistently.")
        a=self.strip(DATA,1.05,.72).move_to(LEFT*3.5+UP*1.1); c=self.code(["scores.mean()       # 79.83","scores.sum()        # 479","scores.min()        # 66","scores.max()        # 90","scores.std()        # 8.69 population","scores.std(ddof=1) # 9.52 sample"],7.0,"DESCRIPTIVE STATISTICS",21).move_to(RIGHT*3.65+DOWN*.4)
        n=self.note("STANDARD DEVIATION",["np.std(x): population SD","np.std(x, ddof=1): sample SD","Use the definition required by the problem."],6.0,21).move_to(LEFT*3.5+DOWN*1.5)
        self.play(FadeIn(a),FadeIn(c),run_time=RN); self.wait(WR); self.play(FadeIn(n),run_time=RN); self.wait(WW); self.clear()
    def filtering(self):
        self.head(7,"FILTER DATA WITH A CONDITION","Boolean indexing selects only observations that satisfy a condition.")
        a=self.strip(DATA,1.08,.74).move_to(UP*1.05); b=VGroup(*[self.tx(x,19,True,True) for x in ["False","True","True","False","False","True"]]).arrange(RIGHT,buff=.32).move_to(DOWN*.05); self.fit(b,7,.5)
        c=self.code(["mask = scores >= 80","scores[mask]","# array([85, 90, 88])"],6.3,"BOOLEAN INDEXING",24).to_edge(DOWN,buff=.28)
        self.play(FadeIn(a),run_time=RN); self.play(Write(b),FadeIn(c),run_time=RN); hi=[SurroundingRectangle(a[0][i][0],buff=.04,color=INK,stroke_width=4) for i in (1,2,5)]; self.play(LaggedStart(*[Create(x) for x in hi],lag_ratio=.15),run_time=RN); self.wait(WW); self.clear()
    def summary(self):
        self.head(8,"A REPRODUCIBLE ARRAY WORKFLOW","Use the same sequence every time you receive a dataset in Colab.")
        steps=[("1","IMPORT NUMPY"),("2","CREATE ARRAY"),("3","CHECK SHAPE / DTYPE"),("4","INDEX OR SLICE"),("5","FILTER IF NEEDED"),("6","CALCULATE STATISTICS")]; cards=VGroup()
        for n,t in steps:
            box=self.panel(4.3,1.25,WHITE); lab=self.fit(self.tx(t,20,True),3.3,.44); cards.add(VGroup(box,VGroup(self.tx(n,24,True),lab).arrange(RIGHT,buff=.22).move_to(box)))
        cards.arrange_in_grid(rows=2,cols=3,buff=(.35,.38)).move_to(DOWN*.15); take=self.tx("ARRAY = VALUES + ORDER + INDEX + SHAPE",30,True,True).to_edge(DOWN,buff=.3)
        self.play(LaggedStart(*[FadeIn(x,shift=UP*.1) for x in cards],lag_ratio=.1),run_time=2); self.wait(WE); self.play(Write(take),run_time=RN); self.wait(3.5); self.play(*[FadeOut(m) for m in self.mobjects],run_time=RN)
        end=VGroup(self.tx("STATISTICS 11 · GOOGLE COLAB",25,True),self.tx("Arrays turn raw observations into computable data.",38,True),self.tx("Define · Inspect · Select · Calculate · Interpret",25)).arrange(DOWN,buff=.28); self.fit(end,13.5,4); self.play(FadeIn(end,shift=UP*.1),run_time=RN); self.wait(3.5); self.play(FadeOut(end),run_time=RN)
