# PA-Power-Prices


## About:
3 functions are included in this program:
1. Main function that serves as the driver, exports results as a csv at the end
2. getRates(): contains our selenium portion of the code. This function takes a zipcode, navigates to papowerswitch.com and downloads the resulting csv file
3. importResults(): processes the downloaded results file from the getRates() function, adds a date, zipcode, and provider column, and then appends the resulting data to the full data of all zip codes for that day

## Contacts:
[Alberto Lamadrid, Ph.D.](https://business.lehigh.edu/directory/alberto-j-lamadrid) ,  Lehigh University, Economics, Associate Professor

[Henry Eaton](hhe223@lehigh.edu), Student, Lehigh University

### References:
[Selenium WebDriver Documentation](https://www.selenium.dev/documentation/webdriver/)

[Link to updated list of zip codes in PPL Electric Region](https://www.pplelectric.com/-/media/PPLElectric/At-Your-Service/Docs/General-Supplier-Reference-Information/PPLServicingArea-Zipcodes.xls)
