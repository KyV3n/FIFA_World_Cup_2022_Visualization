## Implementation details
During the project we made use of the following websites and libraries to help with the visualization project:

- To help us with creating a multipage dash site, we used the following site: [Dash Multi Page](https://medium.com/@mcmanus_data_works/how-to-create-a-multipage-dash-app-261a8699ac3f)
- We used the following libraries: [Requirements](#requirements)
- While creating the Dash app, we made use of the documentation provided by Dash: [DASH](https://dash.plotly.com)

For defenders page:

- Splitting age bracket: Rounding float numbers up and down to the nearest integer number:  [Round Integer](https://stackoverflow.com/questions/43851273/how-to-round-float-0-5-up-to-1-0-while-still-rounding-0-45-to-0-0-as-the-usual)
  - Answer from user 'EquipDev' was used
- Splitting age bracket: Getting list of lists for even splits based on amount of years: [Split Years](https://codereview.stackexchange.com/questions/214857/split-a-number-into-equal-parts-given-the-number-of-parts)
  - Answer from user 'SylvainD' was used and slightly modified by us
- Violin & Scatter plots: Get indices of NaN values: [Index NaN](https://blog.finxter.com/how-to-find-dataframe-row-indices-with-nan-or-null-values/)
  - Method 2 was used
- Scatterplot: Hiding dcc component based on value in dropdown menu: [Hide Component](https://stackoverflow.com/questions/67960035/how-to-create-dynamic-dropdown-based-on-user-multi-value-of-another-dropdown-in)
  - Answer from user 'zerOpRiME' was partly used
- Scatterplot (Teams): Limit amount of selected values in multi-dropdown menu: [Max Selection](https://community.plotly.com/t/dash-multi-dropdown-menu-limit/7921/6)
  - Answer from user 'dhepper' was used
- Scatterplot Fit Line: How to fit a quadratic curve and add its trace to the scatterplot: [Bing Copilot](https://www.bing.com/search?toncp=0&q=Bing+AI&showconv=1)
  - Query: Please give me code on how to make a scatter plot with quadratic fit lines in Python using Dash
  - fit_quadratic_curve(x,y) function and line after '# Add quadratic fit line' were used from the answer
- Color palette for violin plot and multi scatterplot: [Color Palette Generator](https://venngage.com/tools/accessible-color-palette-generator)
  - Used code #02C199, then the Vibrant palette