---
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-5:
    identifier: cenm-1-5-release-notes-ja
    parent: cenm-1-5-cenm-releases
    weight: 81
tags:
- release
- notes
title: Release notes (Japanese)
---


# Corda Enterprise Network Managerリリースノート

## Corda Enterprise Network Manager 1.5

Corda Enterprise Network Manager (CENM) 1.5では、新しい[CENM管理コンソール](cenm-console.md)、CENMの管理コンソールへのAzure ADを用いたシングルサインオン、ノード鍵（Legal Identity）とその証明書をローテーションする機能など、多くの新機能と機能強化が導入されています。

今回のリリースには後方互換性がありますが、Corda Enterprise Network Managerの以前のバージョンからのアップグレードをご検討ください。

{{< warning >}}
[Corda Enterprise Network Managerのアップグレード](upgrade-notes.md)のページを必ずご確認ください。
{{< /warning >}}

### 新機能と機能強化

#### CENM管理コンソール

[CENM管理コンソール](cenm-console.md)は、CSRやCRRのリクエストを確認し、Network Map上でNodeを表示し、Cordaネットワークの設定値変更（Flag Day）を実施し、サービス構成をアップデートできる、CENMの新しいウェブインターフェースです。

#### Azure ADを使ったシングルサインオン

CENM 1.5 では、CENM [Authサービス](auth-service.md)用のシングルサインオン（SSO）として、Azure Active Directory（AAD）のサポートを導入しています。完全なロールベースアクセス制御（RBAC）をサポートし、システム管理者がユーザーグループや権限を作成し、管理できるウェブベースの管理インターフェースを提供します。[この結果](azure-ad-sso.md)、Azure ADとCorda Authサービスで簡単な設定を行うだけで、CordaサービスとAzure AD間でSSO設定を運用できるようになりました。

#### 証明書ローテーション：ノード鍵（Legal Identity）とその証明書をローテーションする機能

Corda Enterprise 4.7では、ノード鍵（Legal Identity）とその証明書をローテーションする機能を導入しています。これによって、CENMがNetwork Map上において、新しい証明書を使ってNode（Notary Nodeを含む）を再登録できるようになります。

{{< warning >}}
本機能の導入によって、お使いのシステムで証明書ローテーション機能を利用する予定の有無にかかわらず、独自構築したIdentity Managerワークフロープラグインがある場合、プラグインの改造が必要になる場合があります。.[Corda Enterprise Network Managerのアップグレード](upgrade-notes.md)のページを必ずご確認ください。
{{< /warning >}}

本機能の詳細については、[R3サポート](https://www.r3.com/support/)までお問い合わせください。

### 修正された問題

* 約1300以上のNodeが登録されていると、Network Mapサービスの更新が滞る問題を修正しました。
* Kubernetesクラスター上でCENMを展開する際に、Network Mapサービスが完全に起動しない問題を修正しました。

### 既知の問題

* CENMコマンドラインインターフェース（CLI）ツールを使ってNetwork Mapを展開する際に、Network Mapの署名プロセスが失敗し以下のエラーが表示される場合があります：「No NETWORK\_PARAMETERS type signing process set up」この問題を回避するには、AngelサービスとSigningサービスを停止し、手動でプロセスを終了`signer.jar`します。
* 非同期の署名に使った場合、CENMコマンドラインインターフェース（CLI）ツールの署名要求`status`コマンドが失敗します。
* ネットワークパラメータ（`./cenm netmap netparams update cancel`）をキャンセルするためにCENMコマンドラインインターフェース（CLI）ツールのコマンドを実行してもメッセージが表示されないので、実行に成功したかどうかがわかりません。
* CRRツールで取り消し申請の要求を実行した後、CRLの署名について十分な取り消しの詳細が表示されません。
* コマンドを`signer`実行するときにトークンが失効していても、CENMコマンドラインインターフェース（CLI）ツールはメッセージを表示しません。
* `workflow.enmListener.port`パラメータが存在しないときに、Identity Managerサービスが間違ったエラーを表示します。
* Shellサポートを使ってCENMサービスを設定している際に、`shutdown`コマンドを実行するとSigningサービスとNetwork Mapサービスがハングします。
* JIRAワークフローを通じて1から11の[拒否コード](workflow.md#certificate-signing-request-rejection-reasons)でCSRが拒否されたとき、Nodeの通知が不正確です。`Additional remark`フィールドの出力に、拒否理由の説明ではなく技術的データが含まれます。

{{< note >}}
上記のリストでは、CENM 1.5に特有の既知の問題を記載しています。過去のバージョンに特有の既知の問題については、このページの下部に記載している、以前のCENMのリリースについてのリリースノートをご覧ください。
{{< /note >}}
