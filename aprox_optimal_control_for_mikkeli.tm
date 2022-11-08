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

  Given time-series, we have value for each per year so <math|\<Delta\>t=1>
  and we have linear equation <math|\<Delta\>\<b-x\>=\<b-A\>*\<b-x\>> from
  datapoints which we can solve using linear optimization.

  After solving for <math|\<b-A\>>. Target change to Mikkeli's parameters
  needs to be solved. We have <math|\<b-y\>=\<Delta\>\<b-x\>> which we want
  to maximize within one year from target values <math|\<b-x\>>. We minimize
  <math|e<around*|(|\<b-Delta\>|)>=<frac|1|2><around*|\<\|\|\>|\<b-A\><around*|(|\<b-x\>+\<b-Delta\>|)>-\<b-y\>|\<\|\|\>><rsup|2>>,
  by derivating

  <math|<frac|d*e<around*|(|\<b-Delta\>|)>|d*\<b-Delta\>>=<around*|(|\<b-A\><around*|(|\<b-x\>+\<b-Delta\>|)>-\<b-y\>|)><rsup|T>\<b-A\>=\<b-0\>>
  <math|\<Rightarrow\>> <math|\<b-Delta\>=<around*|(|\<b-A\><rsup|T>\<b-A\>|)><rsup|-1><around*|(|\<b-A\><rsup|T>\<b-y\>-\<b-A\><rsup|T>\<b-A\>*\<b-x\>|)>>.

  \;

  In pratice, <math|\<b-y\>> is selected to increase työllisyysaste
  (employment rate) by 5%.

  \;

  Update: our target is <math|\<b-y\>=\<b-A\>*\<b-x\>+\<b-Delta\>\<b-x\>> so
  we also use predicted next step parameters as target values. With this
  choice of <math|\<b-y\>>, we have <math|*\<b-Delta\>=\<b-A\><rsup|-1>\<b-Delta\>\<b-x\>>.
  This gives slightly different results.\ 

  \;

  TODO: Generate 2nd derivates from <math|\<b-x\><around*|(|t|)>> time-series
  variables in order to vector in order to possible have sinusoidal complex
  eigenvalue solutions in a solution set.

  \;

  \;
</body>

<\initial>
  <\collection>
    <associate|page-medium|paper>
  </collection>
</initial>