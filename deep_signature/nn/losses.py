# torch
import torch


class ContrastiveLoss(torch.nn.Module):
    def __init__(self, mu=1):
        super(ContrastiveLoss, self).__init__()
        self._mu = mu

    def forward(self, output, batch_data):
        v = output[:, 0, :]
        v2 = v.unsqueeze(dim=1)
        v3 = v2 - output
        v4 = v3.abs().squeeze(dim=2)
        v5 = v4[:, 1:].squeeze(dim=1)
        labels = batch_data['labels'].squeeze(dim=1)
        penalties = labels * v5 + (1 - labels) * torch.max(torch.zeros_like(v5), self._mu - v5)
        return penalties.mean()


class TupletLoss(torch.nn.Module):
    def __init__(self):
        super(TupletLoss, self).__init__()

    def forward(self, output, batch_data):
        v = output[:, 0, :]
        v2 = v.unsqueeze(dim=1)
        v3 = v2 - output
        v4 = v3.abs().squeeze(dim=2)
        v5 = v4[:, 1:]
        v6 = v5[:, 0]
        v7 = v6.unsqueeze(dim=1)
        v8 = v7 - v5
        v9 = v8[:, 1:]
        v10 = v9.exp()
        v11 = v10.sum(dim=1)
        v12 = v11 + 1
        v13 = v12.log()
        return v13.mean(dim=0)


class SignedTupletLoss(torch.nn.Module):
    def __init__(self, exact_examples_count=1):
        self._exact_examples_count = exact_examples_count
        super(SignedTupletLoss, self).__init__()

    # def forward(self, output, batch_data):
    #     k = self._exact_examples_count + 1
    #     v = output[:, 0, :]
    #     v2 = v.unsqueeze(dim=1)
    #     v3 = v2 - output
    #     v4 = v3[:, 1:k, :]
    #     v5 = v3[:, k:, :]
    #     v6 = 10 * v4.abs()
    #     v7 = batch_data['factors'][:, k:].unsqueeze(dim=2)
    #     v8 = v5.sign()
    #     v9 = v5 * (v7 * v8)
    #     v10 = v6 - v9
    #     v11 = v10.exp()
    #     v12 = v11.sum(dim=1)
    #     v13 = v12 + 1
    #     v14 = v13.log()
    #     return v14.mean(dim=0)

    # def forward(self, output, batch_data):
    #     # k = self._exact_examples_count + 1
    #     v = output[:, 0, :]
    #     v2 = v.unsqueeze(dim=1)
    #     v3 = v2 - output
    #     v4 = v3[:, 1:, :]
    #     # v5 = v3[:, k:, :]
    #     v6 = v4.abs()
    #     # v7 = batch_data['factors'][:, k:].unsqueeze(dim=2)
    #     # v8 = v5.sign()
    #     # v9 = v5 * (v7 * v8)
    #     # v10 = v6 - v9
    #     v11 = v6.exp()
    #     v12 = v11.sum(dim=1) / float(v4.shape[1])
    #     # v13 = v12 + 1
    #     v14 = v12.log()
    #     return v14.mean(dim=0)

    # def forward(self, output, batch_data):
    #     # k = self._exact_examples_count + 1
    #     v = output[:, 0, :]
    #     v2 = v.unsqueeze(dim=1)
    #     v3 = v2 - output
    #     v4 = v3[:, 1:, :]
    #     # v5 = v3[:, k:, :]
    #     # v6 = v4.abs()
    #     v7 = batch_data['factors'][:, 1:].unsqueeze(dim=2)
    #     v8 = v4.sign()
    #     v9 = -v4 * (v7 * v8)
    #     # v10 = v6 - v9
    #     v11 = v9.exp()
    #     v12 = v11.sum(dim=1)
    #     v13 = v12 + 1
    #     v14 = v13.log()
    #     return v14.mean(dim=0)

    def forward(self, output, batch_data):
        v_1_3 = output[:, 0, :].unsqueeze(dim=1) # 1:3
        v_2_4 = output[:, 1, :].unsqueeze(dim=1) # 2:4
        v_3_5 = output[:, 2, :].unsqueeze(dim=1) # 3:5
        v_1_4 = output[:, 3, :].unsqueeze(dim=1) # 1:4
        v_2_5 = output[:, 4, :].unsqueeze(dim=1) # 2:5
        v_1_5 = output[:, 5, :].unsqueeze(dim=1) # 1:5

        v_1_2 = output[:, 6, :].unsqueeze(dim=1) # 1:2
        v_2_3 = output[:, 7, :].unsqueeze(dim=1) # 2:3
        v_3_4 = output[:, 8, :].unsqueeze(dim=1) # 3:4
        v_4_5 = output[:, 9, :].unsqueeze(dim=1) # 4:5

        v_1_3_sum = v_1_2 + v_2_3
        v_2_4_sum = v_2_3 + v_3_4
        v_3_5_sum = v_3_4 + v_4_5
        v_1_4_sum = v_1_2 + v_2_3 + v_3_4
        v_2_5_sum = v_2_3 + v_3_4 + v_4_5
        v_1_5_sum = v_1_2 + v_2_3 + v_3_4 + v_4_5

        # diff_1 = v_2_5_sum - v_1_5_sum
        # diff_2 = v_1_4_sum - v_1_5_sum
        #
        # diff_3 = v_3_5_sum - v_2_5_sum
        # diff_4 = v_2_4_sum - v_2_5_sum
        #
        # diff_5 = v_2_4_sum - v_1_4_sum
        # diff_6 = v_1_3_sum - v_1_4_sum

        diff = torch.cat((v_2_5_sum - v_1_5_sum,
                          v_1_4_sum - v_1_5_sum,
                          v_3_5_sum - v_2_5_sum,
                          v_2_4_sum - v_2_5_sum,
                          v_2_4_sum - v_1_4_sum,
                          v_1_3_sum - v_1_4_sum,
                          v_1_2 - v_1_3_sum,
                          v_2_3 - v_1_3_sum,
                          v_2_3 - v_2_4_sum,
                          v_3_4 - v_2_4_sum,
                          v_3_4 - v_3_5_sum,
                          v_4_5 - v_3_5_sum), dim=1);


        v10 = torch.cat((v_1_3, v_1_3_sum, v_2_4, v_2_4_sum, v_3_5, v_3_5_sum, v_1_4, v_1_4_sum, v_2_5, v_2_5_sum, v_1_5, v_1_5_sum), dim=1).abs()
        v11 = v10[:, 0::2, :]
        v12 = v10[:, 1::2, :]
        v13 = (v11 - v12).abs()
        v14 = v13.exp()
        v15 = v14.mean(dim=1)
        v16 = v15.log()

        diff_2 = diff.exp();
        diff_3 = diff_2.mean(dim=1);

        return v16.mean(dim=0) + diff_3.mean(dim=0)


class NegativeLoss(torch.nn.Module):
    def __init__(self, factor):
        self._factor = float(factor)
        super(NegativeLoss, self).__init__()

    def forward(self, output, batch_data):
        v = torch.max(-output, torch.zeros_like(output))
        return v.reshape([-1, 1]).mean(dim=0) * self._factor
