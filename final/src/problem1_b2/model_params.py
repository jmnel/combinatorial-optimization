from .task import Task

Task('Installing the construciton site', 2, list(), 0, 0),
Task('Terracing', 16, [0, ], 3, 30),
Task('Construction the foundations', 9, [1, ], 1, 26),
Task('Access roads and other networks', 8, [1, ], 2, 12),
Task('Erecting the basement', 10, [2, ], 2, 17),
Task('Main floor', 6, [3, 4], 1, 15),
Task('Dividng up the changing rooms', 2, [3, ], 1, 8),
Task('Electrifying the terraces', 2, [5, ], 0, 0),
Task('Construction the roof', 9, [3, 5], 2, 42),
Task('Lighting of the stadium', 5, [3, ], 1, 21),
Task('Installing the terraces', 3, [5, ], 1, 18),
Task('Sealing the roof', 2, [8, ], 0, 0),
Task('Finishing the changing rooms', 1, [6, ], 0, 0),
Task('Construction the ticket office', 7, [1, ], 2, 22),
Task('Secondary access roads', 4, [3, 13], 2, 12),
Task('Means of signalling', 3, [7, 10, 13], 1, 6),
Task('Lawn and sport accessories', 9, [11, ], 3, 16),
Task('Handing over the building', 1, [16, ], 0, 0),
Task('Done', 0, [9, 12, 14, 15, 17], 0, 0)

for t in Task.all():
    print(t)
