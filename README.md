# Python Advanced - Final Project - Elastic Band Method 

![grafik](https://user-images.githubusercontent.com/78024843/128179239-1eeed425-9e78-4ed9-9d47-9eab5edebf7c.png)
Source: https://pics.me.me/thumb_tiger-in-the-flightdeck-the-lack-of-context-here-is-thrilling-mark-watney-spacepirate-introductory-60996521.png

This project was dedicated to explore the wild landscape of... Anything which one provides as a .csv-file.
No matter if we talk about arctic water between frozen icebergs, bobbing up and down, rocky hills in front of the Himalaya or dusty desert with suffocating sand, we will be able to plot the right pathway to rescue our princess (which is somehow lost in the mountains, I guess due to Smaug).

We are also able to find a way through the protective trenches and deliver an important cipher to the General:
![grafik](https://user-images.githubusercontent.com/78024843/128180849-e811c2bf-51f2-4247-a5ec-fb19f704f1da.png)

But be advised: This one will put you in great jeopardy and the former soldiers didn't make it... Maybe it would be good to take more time, be more patient and decrease your force constant k!
![grafik](https://user-images.githubusercontent.com/78024843/128180872-12574326-52c2-4205-9378-b83dfadbc190.png)

Sadly, the soldiers which took that way, lost track of their duty and spent their remaining life in the deep Donnerbalken pit.
It would be wise to find a compromise between these ways and deliver your message!
![grafik](https://user-images.githubusercontent.com/78024843/128180981-363eb5f6-ceea-46f1-b287-38c80a89e9f9.png)

Congratulations!
You have now successfully delivered the cipher to the general!
Without you, the whole battalion would have perished in the devastating fire of the enemies mortars...
Luckily, the general is now aware of the hot spots, which are targeted by the enemy and which exactly cross the red planned line of advance.
The general is showing you the new blue route for invasion and gives the command...

![grafik](https://user-images.githubusercontent.com/78024843/128205196-da1df4d9-c7fa-4bef-8374-dbd14e90ab6f.png)



Besides our small adventure is the elastic band or path-over-hills method used to find the minimal energy configuration of a path between two points
and works in the following way:


By giving the necessary parameters in the params class of the params.py file (Size of the system, end points of the band, given landscape,...),
one prepares the program.
These informations are passed to the run() function in el_band_funcs, which starts by calling the mapCreator() with a specified function 
for the landscape or importing an external csv.
After that the band is created and as first step linearly interpolated between the end points.
By the scipy algorithm scipy.optimize.minimize, one obtains the global energy minimum and the corresponding local band points, which are afterwards 
plotted above the landscape as heatmap and exported in a png file.


Have fun :) (Will you discover the easteregg?)