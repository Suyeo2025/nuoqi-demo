# 版本管理规范

## 核心原则
1. **每次修改前先 git tag 当前版本** — `git tag vXX-pre`
2. **修改后用 Claude Code 做 QA** — 不能跳过
3. **QA 通过后才能部署** — 禁止直接 push 未检验的代码
4. **出问题立即回滚** — `git checkout vXX-stable && git push -f`

## Claude Code QA 流程
```bash
cd /tmp/nuoqi-v8
claude --permission-mode bypassPermissions --print \
  '审查 index.html 的最近改动。检查：
   1. 禁词：全球首個/教授/股權/持股/監事/王干文/蔡黎輝
   2. 价格：基础68888/企业118888
   3. HTML 结构完整性（标签闭合）
   4. CSS 无语法错误
   5. JS 无 console error
   6. 图片/音频路径存在
   报告所有问题。' 2>&1 | tail -30
```

## 部署流程
1. `git tag vXX-pre` (保存点)
2. 做修改
3. Claude Code QA
4. Playwright 截图 (desktop + mobile)
5. `git commit` + `git tag vXX-stable`
6. 复制到 /tmp/nuoqi-deploy/
7. `git push`
8. 验证线上

## 回滚
```bash
cd /tmp/nuoqi-deploy
git checkout vXX-stable -- index.html
git commit -m "Rollback to vXX"
git push
```

## 当前稳定版
- v13-stable: 多语言语音 + Labubu 宠物 + AI 员工大图
