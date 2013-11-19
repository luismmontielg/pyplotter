#-*- coding: utf-8 -*-
import itertools

STACK_VALUES =   u'▁▂▃▄▅▆▇'
STACK_VALUES_0 =   u' ▁▂▃▄▅▆▇'
VOID_STR = ' '


class Plotter(object):
    @staticmethod
    def plot(graph, show_x_axis=True,
             head=None, tail=None, label_length=4, padding=0,
             height=2, show_min_max=True, show_data_range=True,
             show_title=True):
        """
        show_x_axis: Display X axis
        head: Show first [head:] elements
        tail: Show last [-tail:] elements
        padding: Padding size between columns (default 0)
        height: Override graph height
        label_length: Force X axis label string size, may truncate label
        show_min_max: Display Min and Max values on the left of the graph
        show_title: Display graph title (if any)
        show_data_range: Display X axis data range
        """
        def __plot(graph):
            def get_padding_str(label, value):
                padding_str = ''
                if  len(label) < label_length:
                    diff = label_length - len(label)
                    padding_str = ' ' * diff
                padding_str2 = ''
                if  len(str(value)) < m:
                    diff = m - len(str(value))
                    padding_str2 = ' ' * diff
                return '%s%s' % (padding_str,padding_str2)
            out = zip(*graph.strings)
            out.reverse()
            if graph.title and show_title:
                print graph.title
            lines = [sep.join(a) for a in out]
            if show_min_max:
                lines[0] = lines[0] + "   -- Max: %s" % str(max(graph.data))
                lines[-1] = lines[-1] + "   -- Min %s" % str(min(graph.data))
            print '\n'.join(lines)
            if graph.labels and show_x_axis:
                print (u'%s' % x_sep.join(['<%s>[%s]%s'
                        % (label[:label_length], str(v),
                            get_padding_str(label, v))
                            for label, v in zip(graph.labels, graph.data)]))
            if show_data_range and graph.labels:
                print 'Data range: %s - %s' % (graph.first_x, graph.last_x)

        graph.clean_range()
        if head:
            graph.head = head
        if tail:
            graph.tail = tail

        if height:
            graph.height = height

        if label_length < 1:
            label_length = 4

        max_label_length = max(map(len, graph.labels or ['']))

        if max_label_length < label_length:
            label_length = max_label_length

        sep = ''
        if padding >= 1:
            sep = ' ' * padding
        m = max(map(len, map(str, graph.data)))  # length of longest value
        x_sep = '  '
        if show_x_axis and graph.labels:
            # 2('[])' + 2('<>') + 1 space
            sep = ' ' * (label_length + 1 + 2 + m + 2)

        __plot(graph)


class Graph(object):
    """
    data - list
    labels - list
    """

    def __init__(self, data=None, labels=None, title=None):
        self._labels = None
        self._data = None
        self._head = None
        self._tail = None

        self.data = data
        self.labels = [str(e) for e in labels]
        self.height = 2  # default 2 lines
        self.title = title

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, value):
        if value and value < 1:
            raise Exception('head should be >= 1')
        if value and self.tail and value > self.tail:
            raise Exception('head should be <= tail')
        if value > len(self._data):
            self._head = len(self._data)
        else:
            self._head = value

    @property
    def tail(self):
        return self._tail

    @tail.setter
    def tail(self, value):
        if value and value < 1:
            raise Exception('tail should be >= 1')
        if value and self.head and self.head > value:
            raise Exception('tail should be >= head')
        self._tail = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if not value or value < 1:
            raise Exception('height should be >= 1')
        self._height = value

    @property
    def labels(self):
        if self.head and self.tail and self.head < self.tail:
            # use as start - end
            return self._labels[self.head:self.tail]
        elif self.head:
            return self._labels[:self.head]
        elif self.tail:
            return self._labels[-self.tail:]
        else:
            return self._labels

    @labels.setter
    def labels(self, value):
        if self.data and value and len(value) != len(self.data):
            raise Exception('labels length must be equal to data length')
        self._labels = value

    @property
    def data(self):
        if self.head and self.tail and self.head < self.tail:
            # use as start - end
            return self._data[self.head:self.tail]
        elif self.head:
            return self._data[:self.head]
        elif self.tail:
            return self._data[-self.tail:]
        else:
            return self._data

    @data.setter
    def data(self, value):
        if self.labels and value and len(value) != len(self.labels):
            raise Exception('data length must be equal to labels length')
        if not type(list()) == type(value):
            self._data = list(value)
        else:
            self._data = value

    def add_labels(labels):
        self.__add_to_coll('labels', labels)

    def add_data(data):
        self.__add_to_coll('data', data)

    @property
    def first_x(self):
        try:
            return self.labels[0]
        except:
            return ''

    @property
    def last_x(self):
        try:
            return self.labels[-1]
        except:
            return ''

    def clean_range(self):
        self.head = None
        self.tail = None

    @property
    def strings(self):
        """
        The structure of the bar graph. A list that contains all the strings
        that build up a bar in the given position. thise strings are inside a
        list, starting from the top level.

        structure: [
            1st bar -> ['1st level str', ..., 'height-1 str', 'height str'],
            2nd bar -> ['1st level str', ..., 'height-1 str', 'height str'],
           ...
            last bar -> ...
        ]
        """

        def get_strings(stack_id, height):
            def _str(i):
                if i == None:
                    return VOID_STR
                return self.__list[i]

            strings = list()
            for level in range(1, height + 1):
                _len = len(self.__list) * level
                if _len > stack_id:
                    idx = stack_id - _len
                    if (-1 * idx > len(self.__list)):
                        idx = None
                elif stack_id >= _len:
                    idx = -1
                else:
                    idx = _len - stack_id
                _s = _str(idx)
                strings.append(_s)
            return strings

        has_0 = min(self.data) == 0
        self.__list = STACK_VALUES
        if has_0:
            self.__list = STACK_VALUES_0
        mapped_values = ([self.__get_stack_id(x, self.data, self.height)
                                                        for x in self.data])
        return ([get_strings(stack_id, self.height)
                        for stack_id in mapped_values])

    def __get_stack_id(self, value, values, height):
        """
        Returns the index of the column representation of the given value

                                                  ▁  ▂  ▃  ▄  ▅  ▆  ▇' ...
                             ▁  ▂  ▃  ▄  ▅  ▆  ▇' ▇  ▇  ▇  ▇  ▇  ▇  ▇  ...
        ▁  ▂  ▃  ▄  ▅  ▆  ▇' ▇  ▇  ▇  ▇  ▇  ▇  ▇  ▇  ▇  ▇  ▇  ▇  ▇  ▇  ...
        0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 ...

        For example given the values: 1, 2, 3, ..., 20, 21:
            And we are looking for the index value of 21:
            This function will return index 20
        """

        def step(values, height):
            step_range = max(values) - min(values)
            return (((step_range / float((len(self.__list) * height) - 1)))
                    or 1)

        step_value = step(values, height)
        return int(round((value - min(values)) / step_value))

    def __add_to_coll(self, prop, value):
        p = getattr(self, prop)
        if p:
            val = itertools.chain(p, value)
        else:
            val = value
        if not type(list()) == type(val):
            val = list(val)
        setattr(self, prop, val)
