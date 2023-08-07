# 🔹 Description
GUI application to __simulate gravitation__ with many options to interact.

## 🔹 Information
This project provides a __basic gravity simulation__ that allows the visualization of planets interacting under the influence of gravitational forces.
However, it is essential to note that this __simulation is highly simplified__ and does not fully reflect the complexities of __real-world__ gravitational phenomena.
It can be used for __basic exploration and visualization__ of gravitational interactions but should not be considered a precise representation of __reality__.

## 🔹 Tips
The maximum __number__ of the planets is set to __25__\
The minimum __mass__ of the planet is set to __50__\
The maximum __mass__ of the planet is set to __1000__\
The minimum __x and y position__ of the planet is set to __-100000__\
The maximum __x and y position__ of the planet is set to __100000__

*Because of that exceeding these values is blocked.*

## 🔹 Features
__Pause button__ - It pauses all planets in their places.\
(During the pause you can use every other feature).\
![pause](https://github.com/BOOMBERT/gravity-simulator/assets/111244602/1f5ec1e1-f65c-4c85-907b-b557339646c7)

__Center of mass button__ - It displays a cross at the center of mass.\
![center of mass](https://github.com/BOOMBERT/gravity-simulator/assets/111244602/35ced95a-0483-4200-8965-2f3682fe11bd)

__Tracer button__ - When enabled, planets will leave visible trails as they move,\
allowing you to track their paths.\
![tracer](https://github.com/BOOMBERT/gravity-simulator/assets/111244602/395e2ac0-75cc-4ff4-bc36-48368c816e41)

__Spawn a planet button__ - It spawns a new planet at a random position within the window.\
(The app considers the window's new size if resized).\
![spawn planet](https://github.com/BOOMBERT/gravity-simulator/assets/111244602/22115d22-e810-4d3e-b247-4baa3d3b96bb)

__Reset the planets button__ - It removes existing planets and create new ones.\
(Resetting the number of planets to its initial number).\
![reset planets](https://github.com/BOOMBERT/gravity-simulator/assets/111244602/a55dcb2b-aa3b-47cf-af0b-20a0484e85ba)

__Remove planet button__ - It removes the selected planet if any is selected,\
but if none is selected it removes the oldest one.\
![remove planet](https://github.com/BOOMBERT/gravity-simulator/assets/111244602/ce9d6fad-34e0-4685-a623-7d149f802d77)

__Center the planets button__ - It moves all planets, including tracers to the center of the window.\
(So it just moves the center of mass to the position of the center of the window.\
If you resize the window it will consider the new center of window).\
![center planets](https://github.com/BOOMBERT/gravity-simulator/assets/111244602/a6fe5869-57c7-4ba1-bc19-762b893e496a)

__Speed slider__ - Adjust the simulation speed using a slider, ranging from 1 (slowest) to 10 (fastest).\
![speed slider](https://github.com/BOOMBERT/gravity-simulator/assets/111244602/da869e80-cbf1-449c-835b-8733712780d8)

__Edit all properties button__ - Edit all properties (x, y position and mass)\
of a selected planet using inputted values in labels.\
![edit all properties](https://github.com/BOOMBERT/gravity-simulator/assets/111244602/509626e5-23aa-45f3-98f2-2ce6dae4e7db)

__Edit a specific property__ - Edit a specific property (x, y position or mass)\
of the selected planet by inputting the value in the label and pressing the Enter key.\
![edit specific property](https://github.com/BOOMBERT/gravity-simulator/assets/111244602/3a0775fd-28f4-4140-93b7-185fb6233415)

__Moving planets__ - Move planets with the mouse by clicking and dragging them.\
![moving planets](https://github.com/BOOMBERT/gravity-simulator/assets/111244602/d83317ca-6ff8-4cd8-99ec-5e63ce0ac5fa)

__Highlighted selected planet__ – The selected planet will be highlighted with a red border\
and the tracers of the selected planet will be red for easier identification.\
![highlighted selected planet](https://github.com/BOOMBERT/gravity-simulator/assets/111244602/9cfed6f8-617d-4477-bd36-3b3578d3dc70)

__Live information about the selected planet__ - Displaying the current information\
(position and mass) of the selected planet.\
![selected planet info](https://github.com/BOOMBERT/gravity-simulator/assets/111244602/4020654e-0d21-4647-a524-192b4ed63b03)

__Live information about the number of planets__ - Displaying the current number of planets in the simulation.\
![number of planets](https://github.com/BOOMBERT/gravity-simulator/assets/111244602/0e815c93-e65d-4430-8e68-75701a48ec35)

## 🔹 Run locally
Clone the project
```bash
  git clone https://github.com/BOOMBERT/gravity-simulator.git
```

Go to the project directory
```bash
  cd gravity-simulator
```

Install the required libraries
```bash
  pip install -r requirements.txt
```

Start the application
```bash
  python main.py
```

\
**You can download this application as an exe file from here:**\
https://drive.google.com/file/d/12Y9CtYrkmccrnc63zl2KOai1bZeFJF8x/view?usp=sharing
