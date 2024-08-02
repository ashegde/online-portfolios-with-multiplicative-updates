# online-portfolios-with-multiplicative-updates

In this example, we investigate the exponentiated gradient algorithm for online optimal portfolio construction as proposed in:

Helmbold, D. P., Schapire, R. E., Singer, Y., & Warmuth, M. K. (1998). On‐line portfolio selection using multiplicative updates. Mathematical Finance, 8(4), 325-347.

A more recent and broader survey of online algorithms for portfolio construction can also be found in:

Li, B., & Hoi, S. C. (2014). Online portfolio selection: A survey. ACM Computing Surveys (CSUR), 46(3), 1-36.

In particular, this latter reference contextualizes and classifies a variety of online algorithms, highlighting core connections between various methods. For example, the exponentiated gradient algorithm falls under the category of momentum methods.

The implementation that I have included here can be run by installing the packages in the `requirements.txt` and evaluating `simulation.py`. In this example, we investigate portfolios made up of stocks from the S&P 500 with a start date of 2005-01-01. Note that the example differs from the above references in this aspect as we look at for more stocks. As such, we find that larger learning rates lead to higher total wealth.

For the majority of strategies tested, we start with a uniform weights across the market. Our best performing algorithm ends up highly concentrated (due to the high learning rate) in the best performing stocks. Are these results realistic? Probably not. For example, things like trading costs are not taken into account.

![portfolio_wealth](https://github.com/user-attachments/assets/4495e26e-5684-49a6-a193-cae2cfb66134)
![holdings_over_time](https://github.com/user-attachments/assets/c8d15999-57b1-4661-9a02-e41b9602459c)

Interestingly, at various time instances, the portfolio becomes rather highly concentrated in certain stocks with high past-day performance. While this in general seems quite risky, and perhaps defies the conventional wisdom of diversification, this behavior is quite precedented. For example, in discussing Kelly-style investing strategies, William Ziemba writes/quotes in:

Ziemba, W. T. (2015). A response to Professor Paul A. Samuelson's objections to Kelly capital growth investing. Journal of Portfolio Management, 42(1), 153.

the following:

> Other examples of investors who behave as if they were full or close to full Kelly investors are Warren Buffett, George Soros and John Maynard Keynes who all have portfolios with the following Kelly characteristics.:
>>"the portfolios are highly concentrated, not diversified, with huge positions in the few very best investments with much monthly variation and many monthly losses but very high final wealth most of the time."

There are a several follow-up directions that I think would be quite interesting.

First, it is clear that tuning hyperparameters such as the learning rate is quite important as it impacts how quickly the algorithm adapts or is reinforced by changes in price relatives. Characterizing the learning rate and its relation to diversification and risk seems useful. In this exponentiated gradient algorithm, this is characterized by the KL divergence penalty between the previous and current weight configurations. 

Second, making things more realistic to account for trading costs, tax implications, liquidity issues and other frictions, etc. This might require constrained optimization approaches akin to those in model predictive control and more general sequential decision algorithms, e.g.,

Boyd, S., Johansson, K., Kahn, R., Schiele, P., & Schmelzer, T. (2024). Markowitz Portfolio Construction at Seventy. arXiv preprint arXiv:2401.05080.

Third, safe and robust inclusion of "approximately correct" probabilistic prediction models, akin to:

Mitzenmacher, M., & Vassilvitskii, S. (2022). Algorithms with predictions. Communications of the ACM, 65(7), 33-35.

Leveraging machine learned models in this capacity could help incorporate side information from alternative data sources.

Fourth (and related to third), incorporation of methods from UQ and active learning.

Fifth, the themes of online optimization of portfolios exist beyond financial markets -- e.g., scientific funding of research projects, ensembles/mixtures of models, etc. Where else can these tools be productively applied?

Lots of new things to learn :)
