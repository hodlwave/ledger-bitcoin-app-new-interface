# Ledger Bitcoin App 2.0 CLI

This tool provides a convenient interface for using Ledger's new [Bitcoin 2.0 app](https://github.com/LedgerHQ/app-bitcoin-new/tree/develop/bitcoin_client) in multisig wallets.

## Example

This example walks through the end-to-end wallet flow for a 2-of-2 multisignature P2WSH wallet on testnet.

Ledger BIP39 Recovery Phrase:
```
1. rabbit
2. wealth
3. way
4. possible
5. road
6. client
7. pottery
8. seek
9. crystal
10. palace
11. anchor
12. quality
13. predict
14. ahead
15. weird
16. anchor
17. whisper
18. stock
19. salmon
20. sleep
21. rally
22. guilt
23. manage
24. beef
```

- Fingerprint: `45d3c07e`
- Derivation Path: `m/48'/1'/0'/2'`
- Extended public key: `tpubDELQKePHiJzWpZixbdm2DhDKxus9YnDWi42MvVKSEv6QD8QqpvuXFxCdtCjxYyFiqXJNUk7XitdPjjcx1Wu2GFYcCCnjrX8bPdcb694Cdkc`

Other BIP39 Recovery Phrase
```
1. shine
2. fit
3. lawn
4. armor
5. spoil
6. undo
7. regret
8. harsh
9. stairs
10. welcome
11. loop
12. energy
```

- Fingerprint: `358977ae`
- Derivation Path: `m/48'/1'/0'/2'`
- Extended public key: `tpubDEkgaW2Z2LMF8VZ58iNjWZ7qizZ6DXsKMQecQQXrdbwdojST74xpLy2jHS7ZKcMieJWXFNphfHvWh5tYJ8C62XwqsNT5pAEQAV5xXiDVRXU`


### Wallet registration

The ledger app requires a `/**` suffix on each descriptor key so remember to add that to each.

```
python3 ledger.py --network testnet register \
  --wallet ledger-testing \
  --threshold 2 \
  --key-expression "[45d3c07e/48'/1'/0'/2']tpubDELQKePHiJzWpZixbdm2DhDKxus9YnDWi42MvVKSEv6QD8QqpvuXFxCdtCjxYyFiqXJNUk7XitdPjjcx1Wu2GFYcCCnjrX8bPdcb694Cdkc/**" \
  --key-expression "[358977ae/48'/1'/0'/2']tpubDEkgaW2Z2LMF8VZ58iNjWZ7qizZ6DXsKMQecQQXrdbwdojST74xpLy2jHS7ZKcMieJWXFNphfHvWh5tYJ8C62XwqsNT5pAEQAV5xXiDVRXU/**"
```

This command should return the policy id and the policy hmac, which is required for securely receiving and sending bitcoin:

```
Policy id: a040e20c8eb4b119144a9a0a0a95d2a901186b9ecb9d6a05d11f10e24b2c6a91
Policy hmac: 7824b8740c2aa9bf18c57b11d6bf9ee3dce48d26ec8c133e672b5599a4b60cfb
```

### Receive Bitcoin

```
python3 ledger.py --network testnet receive \
  --wallet ledger-testing \
  --threshold 2 \
  --key-expression "[45d3c07e/48'/1'/0'/2']tpubDELQKePHiJzWpZixbdm2DhDKxus9YnDWi42MvVKSEv6QD8QqpvuXFxCdtCjxYyFiqXJNUk7XitdPjjcx1Wu2GFYcCCnjrX8bPdcb694Cdkc/**" \
  --key-expression "[358977ae/48'/1'/0'/2']tpubDEkgaW2Z2LMF8VZ58iNjWZ7qizZ6DXsKMQecQQXrdbwdojST74xpLy2jHS7ZKcMieJWXFNphfHvWh5tYJ8C62XwqsNT5pAEQAV5xXiDVRXU/**" \
  --change 0 \
  --index 0 \
  --policy-hmac "7824b8740c2aa9bf18c57b11d6bf9ee3dce48d26ec8c133e672b5599a4b60cfb"
```

The following address should be displayed on-screen and in the terminal after approving it:
```
Receive address: tb1qfjapkasdnjv9m05jlnvju93xg3txxrd2v98q3ppt925mzwep8mzqx8fs0e
```

### Send Bitcoin
We've received the following 2 UTXOs from a Bitcoin Testnet faucet:
```
tb1qfjapkasdnjv9m05jlnvju93xg3txxrd2v98q3ppt925mzwep8mzqx8fs0e: 0.00094760 tBTC
tb1qstduh84r92cvp0cx76fje0cyfycwqnamqlgry9205t9zjqgrw47q4zhfew: 0.00078047 tBTC
```

Let's send 100,000 testnet sats back to the faucet address: `mohjSavDdQYHRYXcS3uS6ttaHP8amyvX78`. Save the base64 psbt file in `ledger-testing-send-to-faucet.psbt`
```
cHNidP8BAKkCAAAAAip0qQkD78Xos492dfsqz3Q13Iv77UBMkFSUP3cu00P9AAAAAAD9////fskHCYqISqDw0IZ0eyQXbmVhFwqMc62fD0qQEmLaK6wBAAAAAP3///8CThsBAAAAAAAiACD/1x8AgnVMB+RBrXZVSuV+bFyZKHmQncPO7kPfZQAdZKCGAQAAAAAAGXapFFnK2lAxTIKeGfWneG+O4NSYf0KdiKx0zCMATwEENYfPBDpVywGAAAAC/hcStvo5LaTCo6xlYFUdst12eUlNn34XQIGFe2V4RQgDbqFiFlW/H+JFGxXlpW63rEh7x+FPXhlvf532SXUOWVwURdPAfjAAAIABAACAAAAAgAIAAIBPAQQ1h88Ec0ohhoAAAALnY0oTGG6PFqDVa/dkfNcPXk7/a4iqHIsVpSQOreyBTQJKK174kgzTne0y2sL0bfi7kqblMqrwQn/UtIXjK7CF5xQ1iXeuMAAAgAEAAIAAAACAAgAAgAABAH0CAAAAAWvQX15YoAlays4//ixnGB6s2sQn+3Pcyr/gDDgmJrpPAAAAAAD+////At8wAQAAAAAAIgAggtvLnqMqsMC/BvaTLL8ESTDgT7sH0DIVT6LKKQEDdXzMQU9xAAAAABYAFAi/pBUGgT9/hDEE6wHy8jQPPsGjdMwjAAEBK98wAQAAAAAAIgAggtvLnqMqsMC/BvaTLL8ESTDgT7sH0DIVT6LKKQEDdXwBAwQBAAAAAQVHUiEDSrdBJPdnl3oIXV7M5AUvSLB8RKaM9UDplOMKd0l5pPghA+x+5XeSi/5v8kDaqJdhqHdzleZYHwdWJ3GL7J/+vtfEUq4iBgNKt0Ek92eXeghdXszkBS9IsHxEpoz1QOmU4wp3SXmk+BxF08B+MAAAgAEAAIAAAACAAgAAgAAAAAABAAAAIgYD7H7ld5KL/m/yQNqol2God3OV5lgfB1YncYvsn/6+18QcNYl3rjAAAIABAACAAAAAgAIAAIAAAAAAAQAAAAABAH0CAAAAAblNm/vw+e8e64kdSnzWnQSwkepFG7p/wjTgGEmztAyrAQAAAAD+////AkxldkcAAAAAFgAUMxtX6mMucKfs6A29a4Mi4VVw60socgEAAAAAACIAIEy6G3YNnJhdvpL82S4WJkRWYw2qYU4IhCsqqbE7IT7EdMwjAAEBKyhyAQAAAAAAIgAgTLobdg2cmF2+kvzZLhYmRFZjDaphTgiEKyqpsTshPsQBAwQBAAAAAQVHUiECN2KBoB3WtbTaruOdhVSGbB3E2P8l1aNNsM92gJ4Zj7AhA0kFjftiAupD2r9klEe3K2H98fG/6DSGcOCQ6pjIMESTUq4iBgNJBY37YgLqQ9q/ZJRHtyth/fHxv+g0hnDgkOqYyDBEkxxF08B+MAAAgAEAAIAAAACAAgAAgAAAAAAAAAAAIgYCN2KBoB3WtbTaruOdhVSGbB3E2P8l1aNNsM92gJ4Zj7AcNYl3rjAAAIABAACAAAAAgAIAAIAAAAAAAAAAAAABAUdSIQJv6naL1IpiTWScuwZWqyL8l/CPwJvr0bJfsd7C0i9QgSEC8/unkj1a33BjRDMeMB/EpFL1Fu6EZ2Msk+B7neO8bvNSriICAvP7p5I9Wt9wY0QzHjAfxKRS9RbuhGdjLJPge53jvG7zHEXTwH4wAACAAQAAgAAAAIACAACAAQAAAAAAAAAiAgJv6naL1IpiTWScuwZWqyL8l/CPwJvr0bJfsd7C0i9QgRw1iXeuMAAAgAEAAIAAAACAAgAAgAEAAAAAAAAAAAA=
```

Run the command on the psbt.
```
python3 ledger.py --network testnet sign \
  --wallet ledger-testing \
  --threshold 2 \
  --key-expression "[45d3c07e/48'/1'/0'/2']tpubDELQKePHiJzWpZixbdm2DhDKxus9YnDWi42MvVKSEv6QD8QqpvuXFxCdtCjxYyFiqXJNUk7XitdPjjcx1Wu2GFYcCCnjrX8bPdcb694Cdkc/**" \
  --key-expression "[358977ae/48'/1'/0'/2']tpubDEkgaW2Z2LMF8VZ58iNjWZ7qizZ6DXsKMQecQQXrdbwdojST74xpLy2jHS7ZKcMieJWXFNphfHvWh5tYJ8C62XwqsNT5pAEQAV5xXiDVRXU/**" \
  --change 0 \
  --index 0 \
  --policy-hmac "7824b8740c2aa9bf18c57b11d6bf9ee3dce48d26ec8c133e672b5599a4b60cfb" \
  --psbt-file ledger-testing-send-to-faucet.psbt
```

After approving the transaction on the ledger device, the terminal should display the signed PSBT, which can be finalized and broadcast to the Bitcoin network.
```
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
```
