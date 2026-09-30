# archive-index-notes.md — SPFC_P6 Curatorial Consolidation + 96-item Archive Index

**Date**: 2026-09-30
**Task**: SPFC_P6_CURATORIAL_ARCHIVE_INDEX
**Author**: Agent (not from memory; all data sourced from canonical Internet Archive item directory)
**Status**: PASS

---

## 1. 数据来源

`catalog-96.json` 不是从记忆补全的。它的来源按优先级：

### 1.1 主源：Internet Archive `metadata.description`（canonical）
- URL: `https://archive.org/metadata/selectedphotographsfromchina`
- 字段: `metadata.description`（HTML，约 23,139 字符；strip tag 后 7,578 字符 plain text）
- 这是 Archive 自身的编辑转录；它把原书的 Contents 页完整列出，每个条目用 `<br>` 分行
- 格式：`Title (colour?) — Credit — PageNum`（em-dash 分隔）
- **优势**：每个条目占一行，结构干净，没有 OCR column-shuffle
- **缺点**：纯文本无行号锚定，不携带叶子号（leaf number）

### 1.2 交叉验证源：Internet Archive `djvu.txt` OCR 文本
- URL: `https://archive.org/stream/selectedphotographsfromchina/selectedphotographsfromchina_djvu.txt`
- 大小: 153,753 字节 / 3,957 行
- Contents 部分在 line 2796 起，约 600-800 行的范围
- **用于交叉验证 metadata.description 中的 Title / Credit 是否与原书 OCR 文字一致**
- OCR 噪点（`(co/our)`、`(cofour)`、`(cc/our)` 等替代 `(colour)`）不进入 catalog-96.json；只承认 metadata.description 中干净的形式

### 1.3 关联源：works.json（18 件当前展览）
- `works.json` 中 18 件作品的 `page` / `leaf` / `author` / `human_verified` 用于 cross-reference：
  - `selected_for_exhibition` flag
  - `printed_credit` 优先用 works.json 的 author（P1-confirmed）
  - `catalog_credit_variant` 来自 works.json 的同名字段（catalog 拼写）

### 1.4 不使用的源
- **不在 metadata.description 中的人为补全**：catalog-96.json 严格 96 条，不增不减
- **不在记忆中的中文摄影者姓名**：所有 credit 保持英文/拼音
- **不在 OCR 噪点里的拼写**：(co/our)、(cofour) 等不进入正文

---

## 2. Transcription 与 OCR 的使用方式

| 字段 | 主源 | 备注 |
|---|---|---|
| `printed_title_en` | metadata.description | 96 条全部来自这里 |
| `printed_credit` | works.json（for 18 件 selected）→ 否则 metadata.description | 18 件 P1-confirmed 用 works.json；78 件文本档案直接用 catalog spelling |
| `catalog_credit_variant` | works.json（仅 p.3/p.52/p.90） | §7 强制保留的 3 个冲突 |
| `colour_marked_in_contents` | metadata.description | 严格以目录是否写 `(colour)` 字面为准 |
| `book_page` | metadata.description 末尾的 page number | 1-100（plate 35/41/53/73 缺号是书的印刷跳过，不是数据缺失） |
| `selected_for_exhibition` | works.json 18 件的存在性 | 其他 78 件 selected=false |
| `scan_asset_available` | works.json 中是否有 leaf 资产 | 仅 18 件扫描资产已 acquire |
| `review_status` / `human_verified` | works.json | 不重新查源；catalog-96.json 只是 works.json 的镜像 |

---

## 3. colour 字段含义

`colour_marked_in_contents` **只回答一个问题**：原书目录是否明确写了 `(colour)`？

- `true` = 目录字面标注 `(colour)`（共 68 条）
- `false` = 目录没有写 `(colour)`（共 28 条）

**`false` 绝不解释成 black_and_white=true**。目录未标 ≠ 黑白；可能是 publisher 决定不强调色彩、可能是印刷阶段丢失标记、可能是目录印刷时漏排。28 条 unmarked 不参与"色彩真实性"判断，只参与"目录是否标注"统计。

如果未来需要判断实际色彩，需要从原页扫描扫描叶做颜色采样，那是单独任务。

---

## 4. title / credit 冲突的处理（§7）

3 个已知冲突保留：
- **p.3**: works.json main = `Chou Chun-yen`；catalog variant = `Chou Chun-jen`
- **p.52**: works.json main = `Chang Chen`；catalog variant = `Chiang Chen`
- **p.90**: works.json main = `Chou Chia-kue`；catalog variant = `Chou Chia-kuo`

`catalog-96.json` 中：
- `printed_credit` ← works.json author（P1-confirmed print spelling）
- `catalog_credit_variant` ← works.json catalog_credit_variant（catalog spelling）

两个值都保留，绝不静默选择一个。Archive Index UI 显示一行 `works.json 'Chou Chun-yen'` / `catalog 'Chou Chun-jen'`，让用户看到冲突。

---

## 5. selected / non-selected 区别

| 字段 | selected_for_exhibition=true (18) | selected_for_exhibition=false (78) |
|---|---|---|
| `scan_asset_available` | true | false |
| `work_page_ref` | "works.json:Plate N" | null |
| `review_status` | AGENT_VISUALLY_REVIEWED 或 HUMAN_VERIFIED | NOT_REVIEWED |
| `human_verified` | 4 件 true (p.3/p.40/p.52/p.90)；14 件 false | 全部 false |
| UI 行为 | 可点击进入 detail dialog；显示 scan asset | 纯文本记录行；无假图片占位 |
| 展览章节归属 | 6 章节（01-06） | 仅在 Archive Index 96 行表中 |

---

## 6. image availability 定义

`scan_asset_available` = 真有真实扫描 JPEG 资产位于 `assets/leaf-NNNN.jpg`，且 works.json 中 `leaf` 字段指向该文件。

- **不依赖任何替代图**（modern photo, AI 生成, 其他照片的历史 OCR 替代图）
- 18 件 selected works 都有真实 leaf-{NNNN}.jpg 资产
- 78 件 text-only 没有扫描 JPEG（`scan_asset_available=false`），Archive Index UI 不显示 placeholder image，只显示文本行

---

## 7. Catalog entry ≠ 视觉核验作品

| catalog entry | 视觉核验作品（exhibition work） |
| --- | --- |
| 96 件（78 + 18） | 18 件（selected_for_exhibition=true） |
| 文本记录 | 真实扫描 + Agent/Human 视觉证据 |
| 可有冲突（多 credit、目录 title 残缺） | 单一代表、当前页面 |
| print spine 拼写 | works.json author（P1-confirmed） |

catalog-96.json 是**目录级**记录。它不等于展览作品。Archive Index UI 让这一点对用户可见——18 行可点击，78 行只是文本。

---

## 8. text record ≠ image acquired

catalog-96.json 的 78 条 text-only 记录：
- **没有** 真实扫描图像
- **没有** thumbnail / placeholder / AI 生成图
- **没有** "其他照片替代" 现代图片

Archive Index UI 中，78 行只显示 book page + English title + credit + colour mark + 状态（"仅文本档案"）。这是 text-only record，与 visual exhibition work 是两个独立层级。

---

## 9. provenance 总结

| 字段类型 | 来源 | 重新核对路径 |
|---|---|---|
| Title / credit / colour mark (96) | metadata.description | Archive canonical |
| p.3/p.52/p.90 冲突保留 | works.json (P1-confirmed) | P1 verification pack |
| 18 selected 关联 | works.json + catalog leaf 资产 | Validator §11 |
| 96 - 18 = 78 text-only | metadata.description | Archive canonical |
| 68 colour-marked | metadata.description 字面 `(colour)` | Archive canonical |
| 28 unmarked | metadata.description 缺字面 | Archive canonical |

如果未来需要重新核对：
1. 拉新 `metadata.description` → 比对 Title/credit/colour 三个字段
2. 拉新 `djvu.txt` → 检查 OCR 是否影响 metadata.description 内容
4. 比对 works.json → 确认 18 件 selected 不变

---

## 10. 不做的事（discipline）

- ❌ 不猜中文摄影者名（catalog 中 credit 全部英文/拼音）
- ❌ 不猜拍摄日期（原书题注没有）
- ❌ 不增删 96 条数量（即使目录中 plate 35/41/53/73 缺号，也不补空条目）
- ❌ 不重新生成 colour 图
- ❌ 不进入 Human Verification P2
- ❌ 不增加第四批 / 第十九件展览作品
- ❌ 不创建新的数据库 / 后台 / 登录
- ❌ 不做 React/Vue迁移（保持静态站）
- ❌ 不重设计网站视觉

---

*Provenance document for SPFC_P6 catalog-96.json + Archive Index UI.*