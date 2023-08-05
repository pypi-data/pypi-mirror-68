# pySEED-EDA
pySEED-EDA is a Python implementation of the **Symmetric-Approximation Energy-Based Estimation of Distribution (SEED) algorithm: A Continuous Optimization Algorithm** [[1]](#1), which allows the optimization in continuous space for independent variable functions, based on distribution estimation algorithms, in the Univariate Marginal Distribution scheme [[2]](#2), the main idea is to make a generational change in each population evolution under the Boltzmann distribution probability function (PDF-B), which is defined by Eq. (1), because PDF-B is a function that has the property that states with less energy are unlikely, so SEED converges in each evolution to a better or equal energy state.
<p align="center"><img src="https://latex.codecogs.com/svg.latex?\Large&space;P_{x} = P(x; {\beta })=\frac {1}{Z} e^{{\beta } g_{x}}\       (1)" title="P_{x} = P(x; {\beta })=\frac {1}{Z} e^{{\beta } g_{x}}\  (1)" /><p>


## References
<a id="1">[1]</a>
J. De Anda-Suárez, J. M. Carpio-Valadez, H. J. Puga-Soberanes, V. Calzada-Ledesma, A. Rojas-Domínguez, S. Jeyakumar, A. Espinal. (2019). Symmetric-Approximation Energy-Based Estimation of Distribution (SEED): A Continuous Optimization Algorithm.
IEEE Access, 7, 154859-154871.

<a id="2">[2]</a>
Brownlee, J. (2011).
Clever Algorithms: Nature-inspired Programming Recipes.
Lulu.com, ISSN:9781446785065.
