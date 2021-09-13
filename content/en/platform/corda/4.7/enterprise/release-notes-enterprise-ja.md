---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-7:
    parent: corda-enterprise-4-7-release-notes
    identifier: corda-enterprise-4-7-release-notes-ja
    weight: 350
tags:
- release
- notes
- enterprise
title: Corda Enterprise release notes (Japanese)
---


# Corda Enterpriseリリースノート

## Corda Enterprise 4.7のリリース概要

今回のリリースでは、数々の新機能と機能強化が導入されているほか、以前のリリースに存在した既知の問題が解決されます。

これまでのリリースでAPIの後方互換性を約束したのと同様に、Corda 4.7でも同じ保証がされています。

Corda 3.0以上で有効なStateやCordappはCorda 4.7でもお使いいただけます。

Corda Enterprise 4.7における主な新機能と機能強化は以下の通りです：

* [アーカイブサービス](#アーカイブサービス)
* [改善されたノータリーのバックプレッシャーメカニズム](#改善されたnotaryのバックプレッシャーメカニズム)
* [ノード管理とフロー管理用の新しい管理コンソール](#node管理とフロー管理用の新しい管理コンソール)
* [証明書ローテーション](#証明書ローテーション)
* [Azure ADへのシングルサインオン](#その他の変更と改善)
* [HSM統合サポート](#その他の変更と改善)
* [HSMに秘密アイデンティティ鍵を保存する機能](#その他の変更と改善)
* [HSM API](#その他の変更と改善)

{{< note >}}
このページでは、Corda Enterprise 4.7に特有の機能のみを記載しています。しかし、Corda Enterpriseのお客様は、Cordaオープンソースリリースの一部としてご利用いただける機能をすべて活用できます。

Corda 4.7の一環として提供される以下のような新機能、機能強化、修正については、[Cordaオープンソースリリースノート](../../corda-os/4.7/release-notes-ja.md)をご覧ください。

* [保証されたステートのリプレイスメントを伴うステートの再発行を行うことで、取引のバックチェーンを断ち切る機能](../../corda-os/4.7/release-notes-ja.md#保証されたステートのリプレイスメントを伴うステートの再発行を行うことで取引のバックチェーンを断ち切る機能)
* [ビジネスネットワークメンバーシップバージョン1.1](../../corda-os/4.7/release-notes-ja.md#ビジネスネットワークメンバーシップバージョン11)
* [新しいマルチRPCクライアントを通じてCordaノードとやり取りをする機能](../../corda-os/4.7/release-notes-ja.md#新しいマルチrpcクライアントを通じてcordaノードとやり取りをする機能)
* [参照アプリケーション：](../../corda-os/4.7/release-notes-ja.md#参照アプリ-bank-in-a-box)
{{< /note >}}

## 新機能と機能強化

### アーカイブサービス

アーカイブサービスは、Node運用者がアウトプットStateを伴わないTransactionの台帳データをアーカイブできるようにする新しいツールです。これによってディスクスペースを節約し、Nodeデータベースへの負荷を削減できます。

アーカイブサービスの機能には以下があります：

* Cordaコマンドラインインターフェース（CLI）コマンドを使ったアーカイブサービスの利用これによって、アーカイブが必要なジョブをすばやく確認し、必要なくなったデータをvaultから削除し、vaultの中身のスナップショットをインポート、エクスポート、復元できるようになります。
* アプリケーションエンティティ―マネージャーを使うと、CorDappsが台帳外のデータベースにアクセスできるようになります。
* アーカイブサービスをCollaborative Recovery [CorDapps](node/collaborative-recovery/introduction-cr.md)と統合すると、壊滅的なシナリオが発生してもデータの復元がスムーズに実行できます。

詳細については[アーカイブサービスの説明](node/archiving/archiving-setup.md)をご覧ください。

### 改善されたNotaryのバックプレッシャーメカニズム

Notaryがトラフィックを扱う方法を最適化するために、Notaryのバックプレッシャーメカニズム（[バックプレッシャーメカニズム](notary/faq/eta-mechanism.md)とも呼ばれます）を更新し、Notaryへの署名リクエストが突然増えた場合のNotaryのパフォーマンスを改善しました。この変更によって、Notaryがタイムアウトする可能性に関する予見精度が向上します。

つまり、「トラフィックの重い状態」でも[高精度かつクイックに動作可能な](notary/notary-load-handling.md)バックプレッシャーメカニズムを実現したことになります。これによってNodeのリトライが削減され、パフォーマンスが最適化され、Node運用者にとってより良いエンドユーザーエクスペリエンスを提供できます。

{{< note >}}
Notaryのバックプレッシャーカニズムとは

設計上、Notaryはトラフィックの負担が極端に大きくても通常通り作動できるようになりました。Notaryのバックプレッシャーメカニズムは、Notaryへの署名リクエストキューを処理し、タイムアウト(大抵はハイトラフィック時)が原因で発生するノードのリトライがNotaryの容量の関数になるよう実現することでこれを可能にしています。このメカニズムによって、必要に応じてそれぞれのNodeが行うノータリゼーションの申請およびリトライにかかる時間や処理能力を確保しています。また、不必要なNodeのリトライによってノータリゼーションの申請キューが不自然に増えることを防ぎ、Notaryの効率性も担保します。
{{< /note >}}

### Node管理とフロー管理用の新しい管理コンソール

Corda Enterprise 4.7には2種類の新しい管理コンソールが搭載されています：

* **Flow管理コンソール**では、ノードで実行されているflowの状態を確認でき、flowに対していくつかの処理を行えます。詳細については、[Flow管理コンソール](node/node-flow-management-console.md)をご覧ください。
* **ノード管理コンソール**では、ノードについての情報を確認でき、いくつかの処理を行えます。詳細については、[ノード管理コンソール](node/management-console/_index.md)をご覧ください。

どちらのコンソールも、CENM [Gatewayサービス](node/gateway-service.md)の一部として動作します。

### 証明書ローテーション

Corda Enterprise 4.7では、ノード鍵（Legal Identity）とその証明書をローテーションする機能を導入しています。これによって、[Corda Enterprise Network Manager](../../cenm/1.5/_index.md)のNetwork Map上において、新しい証明書を使ってNode（Notary Nodeを含む）を再登録できるようになります。本機能の詳細については、[R3サポート](https://www.r3.com/support/)までお問い合わせください。

### その他の変更と改善

* **Azure ADを使ったシングルサインオン**Azure ADとCorda Authサービスで[簡単な設定](node/azure-ad-sso)を行うだけで、CordaサービスとAzure AD間でシングルサインオン（SSO）設定を運用できるようになりました。
* **HSM統合サポート**Corda Enterpriseでは、サポートされていないHSMとCorda Enterpriseインスタンスのユーザーによる統合をサポートするようになりました。今回のリリースには、例として使えるJava実装のサンプルと、展開前に実装をテストできるテストスイートが含まれています。HSM統合の書き方ガイドについては[HSMに関する項](operations/deployment/hsm-integration.md/)をご覧ください。
* **HSMにConfidential Identity鍵を保存する機能**Corda Enterpriseは、nCipher、FuturexとAzure Key VaultのHSMにおけるConfidential Identityに関する鍵の保管をサポートするようになりました。nCipherとAzure Key VaultのHSMではConfidential Identity鍵のネイティブでの利用をサポートし、FuturexのHSMではキーラップモードをサポートします。これらのHSMにおけるConfidential Identity鍵保管の設定については、[HSMに関する項](operations/deployment/hsm-deployment-confidential.md#using-an-hsm-with-confidential-identities/)をご覧ください。
* **HSM API**Corda Enterprise 4.7では、外部のツール開発者がCorda EnterpriseのHSMサポートを拡張するために使える独自のAPIを有するHSMライブラリーが導入されています。
* ネットワークへの初期登録（`initial-registration`）時に、Nodeは`identity-private-key`のエイリアス作成を行うようになりました。詳細については、[Nodeのフォルダ構成](node/setup/node-structure.md#node-folder-structure)の項をご覧ください。これまでは、`cordaclientca`と`cordaclienttls`のエイリアスだけが`initial-registration`中に作成され、`identity-private-key`は初回のNode実行時に必要に応じて生成されていました。そのため、Corda Enterprise 4.7では、`nodekeystore.jks`の内容は通常のNode実行中に変更されません（証明書ディレクトリを事前に設定したキー保管で埋められる`devMode = true`を除きます）。
* Notaryの`batchTimeoutMs`[設定オプション](node/setup/corda-configuration-fields.md#notary)を調整することでパフォーマンス向上を得られる可能性について解説を追加しました。ただし、デフォルト設定は変更されていません。

## プラットフォームバージョン変更

Corda 4.7のプラットフォームバージョンは8から9に引き上げられています。

プラットフォームバージョンの詳細については、[バージョニング](cordapps/versioning.md)をご覧ください。

## 修正された問題

* Accountsを使う際に、Transactionを開始したPartyが受領側のPartyに対して復元を希望する場合に[LedgerSync](node/collaborative-recovery/ledger-sync.md)が差異を出力しない[Collaborative Recovery](node/collaborative-recovery/introduction-cr.md)の問題を修正しました。
* Flowに含まれるメタデータである終了時刻と開始時刻の間で、異なるタイムゾーンを設定できる問題を修正しました。
* ホット／コールドのNodeフェイルオーバーの場合に、カウンターパーティからのメッセージの受領を待っている間に継続的なフローが新しいホットNodeやカウンターパーティのNodeで滞る場合がある問題を修正しました。
* NodeがStateの検索を行う際にいくつかの列挙型をデシリアライズできないためにCorda 4.6 RPCクライアントがCorda 4.7のNodeに対して`NodeFlowStatusRpcOps::getFlowStatus`を実行できない問題を修正しました。
* 入力Stateが10以上あった場合に、`StateRef`は`<hash>:a`として正しくエンコードされるものの、想定される整数入力によって間違ってデコードされるJPA Notaryの問題を修正しました。
* Floatが同じBridgeからの2つの接続の試行を同時に処理し、結果としてバインディングの例外が発生する問題を修正しました。

## 既知の問題

* Nodeの状態のクエリを行う際にいくつかの列挙型をデシリアライズできないために、Corda 4.6 RPCクライアントはCorda 4.7のNodeに対して`NodeFlowStatusRpcOps::getFlowsMatching`を実行できません。
* 場合によっては、RPCクライアントがNodeとの接続に失敗することがあります。このエラーはスペックの低いマシンを使っている場合に発生しやすいです。
* HA UtilitiesツールがLegal IdentitiesやTLS鍵を念頭に実装されているため、`freshIdentitiesConfiguration`についての情報を記録しません。
* HA Utilitiesツールは、`NATIVE`モードを使っている場合、マスター鍵が不要だと記載したメッセージを記録しません。こうしたメッセージは、`initial-registration`コマンドを使ってNodeを登録している場合に、Nodeログにのみ記録されます。
* `NATIVE`モードでのConfidential Identityにはマスター鍵が不要のため鍵は生成されていないにもかかわらず、`NATIVE`モードでのHSMのConfidential Identityを使ったNode登録中に、HA Utilitiesツールのログに「Confidential Identityのキーラップを作成しました」という間違ったログエントリーが含まれます。
* 入力や参照のないTransactionは、出力Stateについて異なるNotaryを有することがあります。その結果、Transactionを発行しているNodeが、そのNotaryとのTransactionのノータリゼーションを行うことなく、出力Stateに任意のNotaryを設定することがあります。
* Azure KeyVaultのサポートについて、Cordaはまだ、古くなったAzure Java SDKバージョン（1.2.1）に依存しています。これによって、Node運用者が`shadedJar`を自身で構築する必要が生じる場合があります。
* 新しいフロー管理コンソールにおいて、ページのリロード後に、フィルターが適用されていた時と同じ結果を表示せず、列のフィルタリング／ソートが間違ってリセットされることがあります。
* 新しいフロー管理コンソールとNode管理コンソールにおいて、ユーザーの名前が短すぎると「パスワードの変更」／「ログアウト」のドロップダウンメニューがすべて見えない場合があります。
* 新しいフロー管理コンソールにおいて、「フローのクエリ」ページ上のカレンダー内の「フローの開始から／まで」のフィールドは2回クリックしないと開けません。
* Collaborative Recovery1.1（または1.0）のイニシエーターは、Collaborative Recovery1.2のレスポンダーによってアーカイブされたTransactionを復元しようとした場合に失敗することがあります。
* （今回のリリースで導入された）証明書ローテーションを実行するとき、`previousIdentityKeyAliases`のリストにない古い鍵によって署名されたStateを使おうとするとフローにエラーが発生して失敗することがあります。
* Health Check Toolは常に、現在のディレクトリではなくCorda Nodeのディレクトリに報告書を保存しようとします。Corda Nodeのディレクトリへの書き込み権限がないNode運用者にとって問題となる可能性があります。
* Corda HSM Technology Compatibility Kit (TCK)テストのコンソールヘルプと[Corda shell](node/operating/shell.md) CLIのヘルプで、フォーマットが一貫していないところがあります。
* `samples:attachment-demo:deployNodes`を実行する際、`serviceLegalName`ではなく`myLegalName`をノータリゼーションに使うため、`runSender`のタスクが添付の送信に失敗します。
* [カスタムIOU CorDapp](https://github.com/corda/production-qa-steps/tree/toropovd/rpc-client/rpc-client/cordapp-example)を移行するために`run-migration-scripts --core-schemas --app-schemas`を実行する際、MS SQLデータベースで動作していると移行スクリプトが失敗します。H2、PostgreSQLとOracleのデータベースに対しては、移行が問題なく動作します。
* 場合によって、カウンターパーティがダウンしている場合やフローが遮断された場合でもNodeがカウンターパーティへの再接続を試み続けることがあります。

{{< note >}}
上記のリストでは、Corda Enterprise 4.7に特有の既知の問題を記載しています。過去のバージョンに特有の既知の問題については、このページの下部に記載している、以前のCorda Enterpriseのリリースについてのリリースノートをご覧ください。
{{< /note >}}
