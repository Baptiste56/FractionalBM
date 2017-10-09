# FractionalBM

Imperial summer thesis project. Tutor : Antoine (Jack) Jacquier.

### How to set up the project:

 * First, download the whole project to a new root file.
 * Then in the LoadDataOpt.py file please change the following lines with your root file adress:
   * 16 : os.chdir("/Users/portenardbaptiste/Python") to os.chdir("/YourRootFile")
   * 30 : os.chdir("/Users/portenardbaptiste/Python/one_dim_1_1000") to os.chdir("/YourRootFile/one_dim_1_1000")
   * 56 : os.chdir("/Users/portenardbaptiste/Python/one_dim_1_1000") to os.chdir("/YourRootFile/one_dim_1_1000")
 * In FracBro.py do the following changes:
   * 17 : os.chdir("/Users/portenardbaptiste/Python/fracBroVorCell") to os.chdir("/YourRootFile/fracBroVorCell")
 * In Nystrom.py do the following changes:
   * 219, 227, 239 and 249 : os.chdir("/Users/portenardbaptiste/Python/fracBroVorCell") to os.chdir("/YourRootFile/fracBroVorCell")

### How to use this project:
#### First mode : The voronoi cell
In main.py, change the value of NVorCell to the number of Voronoi Cell you wish to see.
You can change the value of the Hurst Parameter H in FracBro.py. Note that you need to pre compute the eigenvalues and eigenvectors for each new value of H. There were already pre computed for H = {0.2, 0.5, 0.8}.

Finally run main.py

#### Second mode : Vanilla option price
set up the parameters for the black and scholes method in test.py by doing :
* 7 : env = Env(x, b=?, sig=?, T=?, S0=?, K=?)

Note that there is default values for each parameter.

In line 9 you can change the number of strata and the number of simulations in the monte carlo method with
```pyhton
print(mc.simulation(*Number of Strata*, *Number of Simulations*))
```

Finally run test.py