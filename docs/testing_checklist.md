# Testing Checklist

## Application startup

- [ ] Virtual environment activates successfully
- [ ] Required packages install successfully
- [ ] Streamlit application starts without an error
- [ ] Dashboard opens in the browser

## Property inputs

- [ ] Property A inputs can be edited
- [ ] Property B inputs can be edited
- [ ] Shared assumptions can be edited
- [ ] Percentage inputs remain within valid ranges
- [ ] Holding period remains within the supported range

## Calculations

- [ ] Mortgage balance decreases over time
- [ ] Mortgage balance does not become negative
- [ ] Vacancy lowers collected rent
- [ ] Higher expenses lower cash flow
- [ ] Higher appreciation increases projected sale value
- [ ] Selling costs reduce net sale proceeds
- [ ] Total profit reflects both cash flow and sale proceeds

## Outputs

- [ ] Summary metrics display
- [ ] Annual projection tables display
- [ ] Comparison charts display
- [ ] Currency and percentage values are formatted correctly
- [ ] Sensitivity analyses update when assumptions change
- [ ] “B Minus A” results use the correct direction

## Final review

- [ ] No Python errors appear in the terminal
- [ ] No temporary or private files are tracked
- [ ] README instructions work from a clean environment
- [ ] Disclaimer is visible