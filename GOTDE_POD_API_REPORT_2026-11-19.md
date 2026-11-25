# gotde.cn Print-on-Demand API — Evaluation Report
# gotde.cn 按需印刷 API — 评估报告

**Project / 项目:** Agroverse ceremonial cacao bar packaging — 50 g
**Prepared by / 编制:** Sophia Truesight (TrueSight DAO) · admin+sophia@truesight.me
**Date / 日期:** 2026-11-19 (rev. 2026-11-20)
**Engine / 引擎:** AiCanvaPy 1.0.0
**Status / 状态:** Trial-stage evaluation. Not wired into a production funnel.

---

## 1. Scope / 范围

**EN** — We evaluated the gotde.cn image-generation API as a means of producing photorealistic packaging mockups for a 81 mm × 163 mm portrait cacao bar. Scope: whether the engine can (a) compose a believable bar mockup from a template plus a text prompt, and (b) accept our own brand mark and place it at a specified position and size.

**中文** — 我们评估 gotde.cn 图像生成 API，用于为 81 mm × 163 mm 竖版可可巧克力包装制作逼真的效果图。评估范围：（a）引擎能否基于模板＋文本提示生成可信的包装效果图；（b）能否接受我们自己的品牌标识，并按指定位置与尺寸放置。

---

## 2. Endpoint & authentication / 接口与鉴权

| Item / 项目 | Value / 值 |
|---|---|
| Base URL / 基础地址 | `https://xiaodeapi.gotde.cn` |
| Transport / 传输 | HTTPS (TLS valid 2026-11-17 → 2027-02-15) |
| Auth / 鉴权 | Header `X-API-Key` |
| OpenAPI spec / 接口规范 | `https://xiaodeapi.gotde.cn/api/v1/openapi.json` — HTTP 200, 326 paths |

### Endpoints used / 使用的接口

| Endpoint | Method | Notes / 说明 |
|---|---|---|
| `/api/v1/templates` | GET | Public, no key. Paginate `?page=&pageSize=100`. 73 templates. / 公开，无需密钥。 |
| `/api/v1/open/package-generate` | POST | The generation path. `application/json` only. / 生成接口，仅接受 JSON。 |
| `/api/v1/open/package-generate/records` | GET | Lists prior renders (id, template_id, logo fields, prompt, created_at). / 历史记录查询。 |

> **Note for integrators / 集成方注意:** the OpenAPI document is served at **`/api/v1/openapi.json`**, not at the domain root. `/openapi.json` and `/api/openapi.json` both return 404. Fetch the spec before coding against this API.
>
> OpenAPI 文档位于 **`/api/v1/openapi.json`**，而非域名根路径。根路径返回 404。

---

## 3. Request schema — logo fields / 请求结构 — Logo 字段

`PackageGenerateRequest` accepts four logo fields. These were confirmed directly from the OpenAPI schema and exercised live.

`PackageGenerateRequest` 包含四个 Logo 字段，均已在 OpenAPI 规范中确认并实测生效。

| Field / 字段 | Type & constraints / 类型与约束 | Meaning / 含义 |
|---|---|---|
| `logo_url` | string, ≤2048 chars, png/jpeg/webp | Public URL of the mark / 品牌标识的公网地址 |
| `logo_base64` | string, ≤12,000,000 chars, optional `data:` prefix | Inline image, mutually exclusive with `logo_url` / 内嵌图片，与 `logo_url` 互斥 |
| `logo_position` | `top-left`, `top-center`, `top-right`, `center-left`, `center`, `center-right`, `bottom-left`, `bottom-center`, `bottom-right` | Default `bottom-center` / 默认底部居中 |
| `logo_width_ratio` | number, 0.05 – 0.60 | Default 0.22, relative to print area width / 默认 0.22，相对于印刷区宽度 |

Other core fields / 其他核心字段: `template_id` (int), `design_coverage` (`label` \| `full`), `width_in`, `height_in`, `print_width_in`, `print_height_in`, `background`, `extra_requirements` (prompt), `count` (1–6).

---

## 4. Transport findings / 传输相关发现

1. **JSON only.** The generation endpoint accepts `application/json` exclusively. `multipart/form-data` returns `400 Input should be a valid dictionary or object` — reproduced **even with no file part attached**, which isolates the cause to the content type rather than to a malformed upload. Artwork therefore cannot be sent as a multipart file; use `logo_url` or `logo_base64`.

   **仅接受 JSON。** 生成接口只接受 `application/json`。`multipart/form-data` 会返回 `400`，且**在完全不附带文件的情况下同样复现**，说明问题源于 Content-Type 本身，而非上传格式错误。因此图片无法以 multipart 形式提交，请使用 `logo_url` 或 `logo_base64`。

2. **`logo_base64` is the practical path** when the mark is not publicly hosted. A 102 KB source JPEG encodes to ~137 KB of base64 — far inside the 12 MB limit.

   **当标识未托管于公网时，`logo_base64` 是可行方案。** 102 KB 的 JPEG 经 base64 编码约 137 KB，远低于 12 MB 上限。

3. **Signed `image_url` links expire quickly.** Download the result immediately after generation.

   **返回的 `image_url` 为限时签名链接**，请在生成后立即下载。

---

## 5. Known limitations / 已知限制

### 5.1 Logo placement is generative, not deterministic / Logo 位置为生成式控制，非精确定位

**EN** — This is the most important caveat. `logo_position` and `logo_width_ratio` are written into the generation prompt and the image is passed to the model as a reference. Alignment is therefore **best-effort, not pixel-precise** — as stated in the API's own description. The response echoes back `logo_url` and `logo_position`, but **an echoed value is not evidence that the mark was rendered at that location**; the output pixels must be inspected.

**中文** — 这是最重要的一点。`logo_position` 与 `logo_width_ratio` 会被写入提示词，图片作为参考图送入模型，因此对齐为**尽力实现，而非像素级精确**——接口自身说明亦如此表述。接口响应会回显 `logo_url` 与 `logo_position`，但**回显值并不代表标识确实渲染在该位置**，必须检查输出像素。

**Implication / 影响:** for print-critical output, keep a deterministic post-composite step rather than relying on engine placement.
**对印刷级成品，应保留确定性的后期合成步骤，不应依赖引擎定位。**

### 5.2 No brand typeface / 无法使用品牌字体

**EN** — The engine synthesises stylised pseudo-glyphs. It does not render a supplied typeface, and it re-invents the letterforms on each render. No prompt wording fixes this. Our approach: suppress the wordmark in the prompt, then composite the real mark.

**中文** — 引擎会合成风格化的伪字形，无法使用指定字体，且每次生成都会重新构造字形，调整提示词无法解决。我们的做法：在提示词中要求不出现文字，再后期合成真实标识。

### 5.3 Output geometry drifts / 输出几何尺寸存在漂移

**EN** — The same `template_id` can return different bar aspect ratios between runs. Measured: template 480 returned aspect 0.54 and 0.48 from near-identical payloads. Every render must be measured; do not assume a fixed canvas.

**中文** — 同一 `template_id` 在不同次生成中可能返回不同的条形比例。实测：模板 480 在近似相同的请求下分别返回 0.54 与 0.48。必须对每张输出单独测量，不可假定画布固定。

### 5.4 Template library fit / 模板库适配度

**EN** — 73 templates: 23 "Pro" (Americana/retro) and 50 "内销" (Chinese classical). None targets ceremonial cacao, Amazonian, or specialty-food branding. Treat gotde as a background/style scaffold; brand identity must come from the prompt.

**中文** — 共 73 个模板：23 个 "Pro"（美式复古），50 个 "内销"（中国古典）。均非针对仪式级可可、亚马逊或精品食品品牌。可将 gotde 视为背景与风格底稿，品牌识别需由提示词承担。

### 5.5 Brand asset resolution / 品牌素材分辨率

**EN** — Our only authorised mark is a 668 × 944 px raster (the trademark-filing copy). This is a ceiling for print-resolution label files and for white-label customer output. This is an internal asset gap, not an engine limitation.

**中文** — 我们目前唯一授权的标识为 668 × 944 像素位图（商标申请用副本），这构成了印刷分辨率标签文件与白标客户输出的上限。这属于我方素材缺口，并非引擎限制。

---

## 6. Measured results / 实测结果

26 renders performed in total (record ids 21–64). The final batch passed the real brand mark via `logo_base64` with position and width ratio set explicitly.

共完成 26 次生成（记录号 21–64）。最终一轮通过 `logo_base64` 传入真实品牌标识，并显式设置位置与宽度比例。

| Record | Template | Coverage | `logo_position` | ratio | Measured bar aspect |
|---|---|---|---|---|---|
| 59 | 480 | label | bottom-center | 0.22 | 0.54 |
| 60 | 482 | label | bottom-center | 0.22 | 0.51 |
| 61 | 452 | label | bottom-center | 0.22 | 0.67 |
| 62 | 472 | label | bottom-center | 0.22 | 0.67 |
| 63 | 536 | label | bottom-center | 0.22 | 0.66 |
| 64 | 480 | label | **top-left** | **0.40** | 0.48 |

All outputs were portrait, consistent with the physical 81 × 163 mm product. An earlier internal measurement reporting landscape output was traced to a defective panel-detection routine on our side, not to the engine.

所有输出均为竖版，与 81 × 163 mm 实体产品一致。此前我方报告称输出为横版，经查证系我方面板检测算法缺陷所致，并非引擎问题。

---

## 7. Open questions for the vendor / 需供应商确认的问题

1. Can `logo_position` be made **deterministic** — i.e. a true compositing placement rather than a prompt instruction? If so, at what tier?
   `logo_position` 能否改为**确定性定位**（真正按坐标合成，而非写入提示词）？若可以，属于哪个版本/档位？
2. Is the asymmetric **aspect-ratio drift** on a fixed `template_id` expected? Is there a parameter to lock the output canvas?
   固定 `template_id` 下出现的**比例漂移**是否为预期行为？是否有参数可锁定输出画布？
3. Can a **custom typeface / wordmark** be supplied as a compositing layer?
   能否以合成图层方式**指定字体或字标**？
4. Is a **vector (EPS/SVG/PDF)** export available for print production, versus raster only?
   是否提供面向印刷生产的**矢量格式（EPS/SVG/PDF）**导出，而非仅位图？
5. What is the **rate limit and cost per render** at production volume?
   生产量级下的**调用速率限制与单张成本**是多少？

---

## 8. Related internal docs / 相关内部文档

- `PRINT_ON_DEMAND_MOCKUP_GENERATION.md` — operational runbook, Approach A composite method
- `PRODUCT_DEVELOPMENT_SPECS.md` — product and packaging specification
- `plans/WHITE_LABEL_IMPLEMENTATION_PLAN.md` — white-label product context
