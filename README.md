# Route Planner Algorithm
In this project I used A\* search to implement something like Google-maps route planning algorithm.
I built it for a graduation project for Udacity prgoram.


## Visualizations
The image above shows a network of roads which spans 40 different intersections/nodes (indexed 0 through 39). 
The algorithm I wrote generats a `path` from `start` to `goal` using the best route possible, taking distance & cost to calucation.

For the existing test in `__main__`, the output for start from node 5 to end in node 34 should be: `[5, 16, 37, 12, 34]`