import pygal          
from pygal.style import LightStyle                                             # First import pygal
bar_chart = pygal.Bar(style=LightStyle)                                            # Then create a bar graph object
bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])  # Add some values


bar_chart.render_to_file('bar_chart.svg')                          # Save the svg to a file