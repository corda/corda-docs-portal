---
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-7:
    identifier: corda-os-4-7-release-notes-ja
    parent: corda-os-4-7-release-notes
    weight: 470
tags:
- release
- notes
title: Release notes (Japanese)
---


# Cordaリリースノート

## Corda 4.7

Corda 4.7のリリースノートへようこそ。今回のリリースでは、いくつかの新機能と機能強化が導入されているほか、以前のリリースに存在した既知の問題の多くが解決されます。

これまでのリリースでAPIの後方互換性を約束したのと同様に、Corda 4.7でも同じ保証がされています。

Corda 3.0以上で有効なStateやCordappはCorda 4.7でもお使いいただけます。

### 新機能と機能強化

#### Stateの再発行を行うことで、取引履歴となるバックチェーンを切断する機能

Stateの再発行は通常、プライバシー上の理由またはパフォーマンスの最適化のために検討されます。こうした運用は、事前に設定したタイミングで対象のStateを抽出し、別のTransactionのOutput Stateとして再発行できるカスタムロジックをCorDappの開発者が書くという手法を使うことで、Cordaでも既に可能となっていました。しかしこの手法では、取引履歴が一定の規模に成長した後に、パフォーマンス上の問題が発生する可能性を開発者が予見できる必要があります。また、実装にあたって、予期せぬ失敗のリスクがありました。

Corda 4.7ではStateを再発行する新しい仕組みを導入し、Transactionチェーンを断ち切ることをプラットフォームでサポートします。Stateの所有者はフローを通してTransactionチェーンを切断でき、Stateの再発行に失敗しない事を保証します。Nodeは、Stateを発行者や関係する他の取引参加者に戻すことで、再発行を実現できます。この再発行の仕組みを開発者は「チェーンスニッピング」と呼びます。今回、Cordaはこのパターンに対して、リスクを極小化したサポートを提供します。Stateが再発行されると、再発行前のTransaction履歴はTransaction決定の一部として共有されなくなります。これによって、とても長いTransactionチェーンを生成するアプリケーションのパフォーマンスが向上し、Stateの履歴に関する情報漏洩の防止に役立ちます。

本機能の詳細については、State[の再発行](reissuing-states.md)をご覧ください。

#### ビジネスネットワークメンバーシップバージョン1.1

Corda 4.7では、[ビジネスネットワークメンバーシップの拡張機能](business-network-membership.md)が強化され、メンバーシップへの一括参加機能、メンバーシップ参加者検索機能、メンバーシップ参加／更新依頼の記録報告機能が追加されました。

#### 新しいマルチRPCクライアントを通じてCorda Nodeをインタラクティブに操作する機能

Corda 4.7では、マルチRPCクライアントと呼ばれる新しいRPCクライアントが追加されました。Nodeの運用者は、マルチRPCクライアントを使って、`net.corda.core.messaging.CordaRPCOps`リモートRPCインターフェースを通じてCorda Nodeとやり取りできます。

詳細については、[Nodeとのやり取り](clientrpc.md)のセクションをご覧ください。

### おすすめのアプリ

#### 参照アプリ： Bank in a Box

[Bank in a Box](../../apps/bankinabox/bank-index.md)は製品化の準備が整った新しい[CorDapp](cordapp-overview.md)で、アカウント、Transactionなど、リテールバンキングに必要なアプリケーションに必要な一般的な機能が含まれています。

アプリはCordaの主な機能を活用できるように設計されています：

- [Accounts Library](https://github.com/corda/accounts/blob/master/docs.md)
- [Schedulable State](event-scheduling.md)
- [オラクル](key-concepts-oracles.md)
- 外部システムとCorDappの統合

一連の[フロー](key-concepts-flows.md)と[API](../../apps/bankinabox/api-guide.md)を使って、Bank in a Boxは銀行内振込、定期振込、貸出実行や、口座機能制限などの機能を提供します。わかりやすいUIと権限設定を含んだ完全なソリューションを、簡単に展開できるようにすべてを[Kubernetesコンテナ](https://kubernetes.io/docs/concepts/containers/)でお届けします。

このアプリケーションには、Cordaを使って銀行業アプリケーションを構築したい開発者向けのベストプラクティスや事例が盛りだくさんです。

### プラットフォームバージョン変更

Corda 4.7のプラットフォームバージョンは8から9に引き上げられています。

プラットフォームバージョンの詳細については、[バージョニング](versioning.md)をご覧ください。


### 修正された問題

* vaultが`OR`組合せ子を使ってクエリを行う際に、クエリの結果が定義された割付け制限未満であっても（つまりページ制限を超過していなくても）フィルター条件が間違って割付けエラーをスローする問題を修正しました。この修正はCorda Enterprise 4.5と4.6にも適用されています.
### 既知の問題

* フローの応答者がビジネスネットワークの許可について十分な確認を行いません。これは、ビジネスネットワークのNodeがBNO許可を間違って扱っていることによる問題の可能性があります。ビジネスネットワークのどのNodeでも、フローを変更し確認をオフにできる可能性があります.

{{< note >}}
上記のリストでは、Corda 4.7に特有の既知の問題を記載しています。過去のバージョンに特有の既知の問題については、このページの下部に記載している、以前のCordaのリリースについてのリリースノートをご覧ください。
{{< /note >}}
