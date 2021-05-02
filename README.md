# spam-filter
a spam filter based on Naive baye's classifer

# sample-run 

<pre>
(base) ➜  spam-filter git:(master) python3 spam-filter.py
                WORD    PROBABILITY GIVEN SPAM    PROBABILITY GIVEN HAM
                ----    ----------------------    ---------------------
                iogo    p|S : 0.017               p|H : 0.00023
        irresistible    p|S : 0.0036              p|H : 0.00023
             stylish    p|S : 0.011               p|H : 0.00023
                              ... ... ...
              critic    p|S : 0.00073             p|H : 0.00046
            desiring    p|S : 0.00073             p|H : 0.00046
          selectable    p|S : 0.00073             p|H : 0.00046


TRAINING DATA DETAILS
---------------------
n_spam: 1368
n_ham : 4360

Enter text you want to check for: Congratulations, you've won a lottery!

The text you entered is a SPAM
with spam probability of 0.94

Want to check another text: [Y/N] ?


Enter text you want to check for: Good morning, Bob!

The text you entered is a HAM
with spam probability of 0.0057

Want to check another text: [Y/N] ?
</pre>