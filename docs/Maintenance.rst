Maintenance
===========

Growth-associated maintenance (GAM) is the ATP cost related to growth. This includes the polymerization cost of each macromolecule. This cost is unaccounted for in the BOF because the model synthesizes the building blocks of each macromolecule in sufficient quantity to reflect the cell composition but not the cost of assembling those building blocks together. The GAM can be calculated experimentally by growing the bacteria on different sources of carbon at different starting concentrations. The carbon source should be the sole source of carbon in the media and its concentration should be measured after a given time. These remaining concentrations along with the excretion products are used by the package to constrain the model and calculate the ATP cost of growth.

Non-Growth associated maintenance (NGAM) is the ATp cost related to all non-growth associated processes.

These ATP costs are generated by BOFdat and given as a dictionary in ouput. The file used to generate these coefficients should be extracted from experimental data on different growth conditions. 


