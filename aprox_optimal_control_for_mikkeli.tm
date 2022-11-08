<TeXmacs|2.1>

<style|generic>

<\body>
  <with|font-series|bold|Approximative Optimal Control Solution>

  Tomas Ukkonen

  \;

  We have time-series <math|\<b-x\><around*|(|t|)>> from municipalies data.
  Assume simple linear dif.eq. model for the time-series and solve for some
  kind of optimal control to have wanted changes.

  <\padded-center>
    <math|<frac|d\<b-x\>|d*t>=\<b-A\>*\<b-x\><around*|(|t|)>+\<b-f\><around*|(|t|)>>
  </padded-center>

  We need to solve for optimal control <math|\<b-f\><around*|(|t|)>> which is
  assumed to be constant <math|\<b-c\>=\<b-A\>*\<b-Delta\>> for simplicity.

  Given time-series, each per year so <math|\<Delta\>t=1>, we have linear
  equation <math|\<Delta\>\<b-x\>=\<b-A\>*\<b-x\>> from datapoints which we
  can solve using linear optimization from the time-series.

  After solving for <math|\<b-A\>>. We have a target change to Mikkeli's
  parameters <math|\<b-y\>=\<Delta\>\<b-x\>> which we want to maximize within
  one year from target values <math|\<b-x\>>. We minimize
  <math|e<around*|(|\<b-Delta\>|)>=<frac|1|2><around*|\<\|\|\>|\<b-A\><around*|(|\<b-x\>+\<b-Delta\>|)>-\<b-y\>|\<\|\|\>><rsup|2>>,
  by derivating

  <math|<frac|d*e<around*|(|\<b-Delta\>|)>|d*\<b-Delta\>>=<around*|(|\<b-A\><around*|(|\<b-x\>+\<b-Delta\>|)>-\<b-y\>|)><rsup|T>\<b-A\>=\<b-0\>>
  <math|\<Rightarrow\>> <math|\<b-Delta\>=<around*|(|\<b-A\><rsup|T>\<b-A\>|)><rsup|-1><around*|(|\<b-A\><rsup|T>\<b-y\>-\<b-A\><rsup|T>\<b-A\>*\<b-x\>|)>>.

  \;

  In pratice, <math|\<b-y\>> is selected to increase työllisyysaste
  (employment rate) by 10%.

  \;

  TODO: Write <with|font-shape|italic|Python> script to calculate this all.
  Generate 2nd derivates from <math|\<b-x\><around*|(|t|)>> time-series
  variables in order to vector in order to possible have sinusoidal complex
  eigenvalue solutions in a solution set.

  \;
</body>

<\initial>
  <\collection>
    <associate|page-medium|paper>
  </collection>
</initial>