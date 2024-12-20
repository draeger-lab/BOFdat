Welcome to the documentation for BOFdat
=======================================

BOFdat is a package to generate biomass objective function (BOF) for genome-scale models (GEM) from experimental data described in |Lachance JC et al|_
The definition of the BOF impacts the quality of phenotypic predictions generated by the model. Often, the BOF is defined using another reconstruction work or from another organism. BOFdat is designed to use experimental data specific to your organism to increase the value and specificity of your model. The easiest way to use BOFdat is to download it via pip install (see install below). A full usage example, reconstructing the BOF for Escherichia coli is available on |GitHub|_
, where the entire source code is also available for developers.

.. _Lachance JC et al: https://doi.org/10.1371/journal.pcbi.1006971
.. |Lachance JC et al| replace:: Lachance JC *et al.*

.. _GitHub: https://github.com/jclachance/BOFdat
.. |GitHub| replace:: GitHub

General Usage and implementation details
----------------------------------------

BOFdat is conceived as a workflow for the construction of the BOF divided in three independent modules defined here as steps. Following steps 1 to 3 sequentially should provide the users with a BOF that matches experimental growth rates and yields a high accuracy of essentiality prediction. Following the workflow is not strictly enforced as each step can be performed independently.

**Step1: Generate the stoichiometric coefficients for major macromolecules.** 

We found that the **macromolecular weight fractions (MWF)** are the major determinant of the stoichiometric coefficients (|Lachance JC et al|_) 
. Hence, we advise modellers to query detailed composition of their|rganism. This signifies determining the absolute dry weight of the cell and the percentage dry weight occupied by the major components: proteins, RNA, lipids, DNA and glycans. For more information on how to obtain this composition experimentally we refer to |Beck AE et al|_

.. _Beck AE et al: https://doi.org/10.3390/pr6050038
.. |Beck AE et al| replace:: Beck AE *et al.*

Although not as critical as MWF, using omics data such as **genomic, transcriptomic, proteomic and lipidomic** processed datasets (as two column .csv files) should precise the computation of the stoichiometric coefficients.

To generate accurate growth rate prediction, obtaining growth and non-growth associated maintenance (GAM and NGAM) ATP costs is usually the most important parameter. Growth rate data on different substrate with quantification of **substrate consumption rate** and **metabolic waste production rate** can be incorporated in Step1 of BOFdat to generate the experimentally determined maintenance costs. We provide an example of such data and we suggest referring to |Monk JM et al|_ for further experimental detail.

.. _Monk JM et al: https://doi.org/10.1038/nbt.3956
.. |Monk JM et al| replace:: Monk JM *et al.*

**Step2: Find inorganic ions and coenzymes and generate their stoichiometric coefficients.**

Coenzymes and inorganic ions can be hard to identify experimentally. BOFdat Step2 takes care of identifying these ions by comparing the reconstructed model with the table of universal biomass components generated by |Xavier JC et al|_

.. _Xavier JC et al: https://doi.org/10.1016/j.ymben.2016.12.002
.. |Xavier JC et al| replace:: Xavier JC *et al.*

**Step3: Find the remaining species-specific metabolic objective and generate their stoichiometric coefficients.** 

Considering that the metabolite composition of the BOF reflects the growth requirements of the organism, it therefore impacts the gene essentiality prediction of the model. BOFdat provides an unbiased way to determine these metabolic objectives using experimental gene essentiality data. This is useful for users desiring to increase or validate the essentiality prediction formulated by the model. Usually this type of data is obtained with high-throughput insertion of transposon or, more rarely, with genome-wide single gene knock-out. For more details on experimental high-throughput transposon insertion see |van Opijnen T et al|_

.. _van Opijnen T et al: https://doi.org/10.1038/nmeth.1377
.. |van Opijnen T et al| replace:: van Opijnen T *et al.*


A good example of genome-wide single gene knock-out is the "Keio collection" for *E. coli* (|Baba T et al|_) 

.. _Baba T et al: https://doi.org/10.1038/msb4100050
.. |Baba T et al| replace:: Baba T *et al.*

Installation
------------

BOFdat can be installed directly using pip::
 
   pip install BOFdat


Citation:
---------

If BOFdat helped in the construction of your biomass objective function or the identification of metabolic objectives, please include the following citation to your work: |Citation|_

.. _Citation: https://doi.org/10.1101/243881
.. |Citation| replace:: Lachance J-C, Monk JM, Lloyd CJ, Seif Y, Palsson BO, Rodrigue S, et al. BOFdat: generating biomass objective function stoichiometric coefficients from experimental data. bioRxiv. 2018. p. 243881. doi:10.1101/243881

Contents
--------

.. toctree::
   :numbered:
   :maxdepth: 2
   
   Getting_started
   BOFdat_step1
   BOFdat_step2
   BOFdat_step3
   API
   license
   help   
   

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
