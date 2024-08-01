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

There are a several follow-up directions that I think would be quite interesting.

First, making things more realistic to account for trading costs, tax implications, etc. This might require constrained optimization approaches akin to those in model predictive control and

Boyd, S., Johansson, K., Kahn, R., Schiele, P., & Schmelzer, T. (2024). Markowitz Portfolio Construction at Seventy. arXiv preprint arXiv:2401.05080.

Second, safe and robust inclusion of "approximately correct" probabilistic prediction models, akin to:

Mitzenmacher, M., & Vassilvitskii, S. (2022). Algorithms with predictions. Communications of the ACM, 65(7), 33-35.

Leveraging machine learned models in this capacity could help incorporate side information from alternative data sources.

Third (and related to second), incorporation of methods from UQ and active learning.

Fourth, the themes of online optimization of portfolios exist beyond financial markets -- where else can these tools be productively applied?

Lots of new things to learn :)
