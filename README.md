# ConnectwisePriceAPI
 Connectwise API price/cost updater from ADI API

# How to use
 To use this you will need to make another .py file that stores company id and key information as well as the companies api url.
 You will need a .js file with the ADI API credentials and variables as well. 
 
 Then you will have a text file with all the vendor skus from ADI that need to be updated.
 Once complete compile this program and it will go through the whole list of products and then stop.

You will need to have NodeJS installed and working as well as all the libraries that python requires. Currently putting the node axios module in the same directory has been the only way this will run without giving it another path to where axios is installed. 
