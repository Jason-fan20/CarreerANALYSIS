with open("total.txt", "r",encoding='utf-8') as f:
    a = f.readlines()
    print(a)


from graphviz import Digraph

dot = Digraph(comment='The Test Table')
# 添加圆点A,A的标签是Dot A
dot.node('ROOT', 'Dot A')
# 添加圆点 B, B的标签是Dot B
dot.node('B', 'Dot B')
# dot.view()
# 添加圆点 C, C的标签是Dot C
dot.node(name='C', label= 'Dot C',color='red')
# dot.view()

# 创建一堆边，即连接AB的两条边，连接AC的一条边。
# dot.view()
# 在创建两圆点之间创建一条边
dot.edge('A1', 'C', 'test')
# dot.view()

# 获取DOT source源码的字符串形式
print(dot.source)
dot.view()
dot.render('test-table.gv', view=True)
