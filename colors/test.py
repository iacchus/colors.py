#!/usr/bin/env python

from color import Color

a = Color(rgb=(51, 51, 102))
b = Color(rgb=(102, 51, 51))

#print(a + b)

#     rgb=tuple(map(lambda x, y: x / float(y), *(zip(a.rgb, b.rgb))))

rgb = tuple(x + y for x, y in zip(a.rgb, b.rgb))

print('rgb:', rgb)
col = Color(rgb=rgb)
print('col:', col)

#print(col.rgb)
