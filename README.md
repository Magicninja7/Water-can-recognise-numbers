# What is this
This is a website that can recognize digits you draw, but not thanks to neural networks, but water!! (its actually a 3-directional bfs, but water sounds cooler). You draw a digit on the canvas (the white square) and click analyze! the popup will show you your number. Another important thing is the graph plotter for each value of k (see "how the algorithm works" if you dont know what that is), in my KNN (k-nearest neighbors) algorithm. 


## How the Algorithm Works

This algorithm analyzes the drawing on the canvas using water to detect and recognize numbers. By spilling it over the number, you see how much is left inside, giving you a parameter. Slice each half into two, and you've got 8 parameters. The 9th parameter is how much water is displaced if the number were to be dropped into a pool of water.

![first 8 params](https://hc-cdn.hel1.your-objectstorage.com/s/v3/5d578f3828063f78ba58780bb90d88cc105d37fe_image.png)
![9th param](https://hc-cdn.hel1.your-objectstorage.com/s/v3/fba294818795552c327f3750df743ee849331e4c_image.png)

Although you cannot visualise 9 dimensions, even using a 2D graph, you can still see where the vectors of each number are grouped.

![2dgraph](https://hc-cdn.hel1.your-objectstorage.com/s/v3/0d0a65eef7725021bc398c333c495bebf38386d9_image.png)

Next, you find the n'th nearest neighbours of your number's vector, and see which number is most common; this is your guess.

![knn](https://hc-cdn.hel1.your-objectstorage.com/s/v3/f0e4f9ea5d39f0e1b911d044031f069fa248621b_image.png)

# Check out [PickentCode YouTube channel](https://www.youtube.com/@PickentCode), this whole idea was his, and the photos above are from his [video](https://www.youtube.com/watch?v=CC4G_xKK2g8). It's really great; go watch it!!! its generally a great channel, 10/10 would watch again.


## different files? what are they for?
- add2_testData and add2_trainingData are both files which allow me to add vectors to test and training data, respectively.
- add_data currently doesnt serve a specific purpous, but it holds many vital functions which are needed in other files, like bfs, water, etc.
- class_tk contains the class that is a py app, where you can draw a number, clear the canvas, and submit it to get your prediction.
- flask_app.py it contains the web aspect of this, like having routing from js files, to knn
- index.html the html file
- index.js the javascript file
- knn.py this file contains the ML part of this, using a knn algorithm (shocking, ik)
- plot_k_accuracy.py tests knn.py for different values of k, from 1 to 5o, using testData, which currently has 20 vectors.
- styles.css for the css
- testData.txt this holds the test vectors
- trainingData.txt this holds the training vectors for the ML algorithm, approx. 150
- vercel.json path for vercel to work
