# -*- coding: utf-8 -*-
"""facelib.py - thu vien dung chung cho skill nns-face-highlight.

Nguon goc decode: tools/facetrack/facetrack.py (da kiem 55/55 lan bat duoc mat
tren 3 video). Giu nguyen thuat toan, chi bo sung:
  - tim model theo thu tu uu tien cua hop dong (resources -> assets -> may)
  - tra ve TAT CA hop mat (de ap luat chon nhieu mat), khong chi hop lon nhat
  - doc frame theo CHI SO frame chinh xac (select=eq(n,N)), khong dung -ss
  - toan bo source ASCII: tranh vo console cp1252 tren may khac

MOI script dung file nay phai goi setup_io() dau tien.
"""
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata

try:
    import numpy as np
except ImportError as _exc:          # may khac co the chua cai numpy
    np = None                        # KHONG duoc crash o day: preflight con
    _NUMPY_ERR = str(_exc)           # phai in duoc bang huong dan cai dat
else:
    _NUMPY_ERR = None

# ---------------------------------------------------------------- hang so model
IN_SIZE = 640            # kich thuoc dau vao det_10g.onnx
STRIDES = [8, 16, 32]
NUM_ANCHORS = 2
DEFAULT_THR = 0.5        # nguong diem tin cay
NMS_THR = 0.4

MODEL_NAME = "det_10g.onnx"
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUNDLED_MODEL = os.path.join(SKILL_DIR, "assets", MODEL_NAME)
HOME_MODEL = os.path.join(
    os.path.expanduser("~"), ".insightface", "models", "buffalo_l", MODEL_NAME)


# ------------------------------------------------------------------------ io
def setup_io():
    """Console Windows mac dinh cp1252 -> se crash khi in duong dan co dau
    (vd 'SourcesEdit_Com' co chu 'o' dau moc). Ep utf-8 va bo qua ky tu la."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def have_numpy():
    return np is not None


def require_numpy():
    """Goi truoc khi dung numpy. Neu thieu -> in khoi huong dan roi exit 1,
    KHONG de traceback roi ra man hinh nguoi dung."""
    if np is not None:
        return
    print("")
    print("=" * 60)
    print("  THIEU 1 THU. LAM THEO CAC BUOC SAU ROI CHAY LAI.")
    print("=" * 60)
    print("")
    print("  1) Chua cai thu vien numpy (de tinh toan hop mat va giai ma model)")
    print("     Chay lenh nay:")
    print("         pip install numpy")
    print("     (bao loi goc: %s)" % _NUMPY_ERR)
    print("")
    print("  Sau khi lam xong, chay lai lenh nay de kiem:")
    print("      python scripts/preflight.py --video \"<video>\"")
    print("")
    sys.stdout.flush()
    sys.exit(1)


def require_onnxruntime():
    """Nhu tren, cho onnxruntime. Chan luon traceback ma chinh onnxruntime
    tu in ra khi numpy hong - do khong phai loi cua skill."""
    buf = io.StringIO()
    old_err, old_out = sys.stderr, sys.stdout
    err = None
    try:
        sys.stderr, sys.stdout = buf, buf
        import onnxruntime  # noqa: F401
    except ImportError as exc:
        err = exc
    finally:
        sys.stderr, sys.stdout = old_err, old_out
    if err is None:
        return
    print("")
    print("=" * 60)
    print("  THIEU 1 THU. LAM THEO CAC BUOC SAU ROI CHAY LAI.")
    print("=" * 60)
    print("")
    print("  1) Chua cai thu vien onnxruntime (de chay model nhan dien mat)")
    print("     Chay lenh nay:")
    print("         pip install onnxruntime")
    print("     Ban CPU nay du dung, khong can card do hoa.")
    print("     (bao loi goc: %s)" % err)
    print("")
    print("  Sau khi lam xong, chay lai lenh nay de kiem:")
    print("      python scripts/preflight.py --video \"<video>\"")
    print("")
    sys.stdout.flush()
    sys.exit(1)


def die(msg, code=1):
    """Bao loi RO RANG roi dung. Khong bao gio im lang bo qua."""
    print("")
    print("LOI: %s" % msg)
    sys.stdout.flush()
    sys.exit(code)


def read_json(path):
    with io.open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, obj):
    d = os.path.dirname(os.path.abspath(path))
    if d and not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=1))


def read_lines(path):
    with io.open(path, "r", encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]


_PUNCT = re.compile(r"[^0-9a-z ]+")


def norm_vi(s):
    """Bo dau tieng Viet + ha chu thuong + bo dau cau.

    Nho ham nay ma danh sach tu nhan manh giu duoc ASCII thuan ma van khop
    voi transcript CO DAU: hai phia deu duoc dua ve dang khong dau truoc khi
    so sanh. 'nhung' khop 'nhung'/'nhu'ng'/chu co dau; 'dau tien' khop 'dau tien'.
    """
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    # chr(273)/chr(272) = chu 'd gach ngang' thuong/hoa. Viet bang chr() de file
    # .py nay giu duoc ASCII thuan (khong bao gio vo encoding tren may khac).
    s = s.replace(chr(273), "d").replace(chr(272), "d")
    s = s.lower()
    s = _PUNCT.sub(" ", s)
    return " ".join(s.split())


# -------------------------------------------------------------------- ffmpeg
def have_tool(name):
    """Tra (co_khong, chuoi_version)."""
    try:
        p = subprocess.run([name, "-version"], capture_output=True, text=True)
    except Exception:
        return False, ""
    if p.returncode != 0:
        return False, ""
    first = (p.stdout or "").splitlines()
    if not first:
        return True, "?"
    parts = first[0].split()
    for i, tok in enumerate(parts):
        if tok == "version" and i + 1 < len(parts):
            return True, parts[i + 1]
    return True, first[0][:40]


def probe(path):
    """Doc thong so video. Raise RuntimeError neu khong doc duoc."""
    if not os.path.isfile(path):
        raise RuntimeError("khong thay file video: %s" % path)
    cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0",
           "-show_entries", "stream=width,height,nb_frames,r_frame_rate,codec_name",
           "-show_entries", "format=duration", "-of", "json", path]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0 or not (p.stdout or "").strip():
        raise RuntimeError("ffprobe khong doc duoc video: %s" % (p.stderr or "").strip()[:300])
    j = json.loads(p.stdout)
    if not j.get("streams"):
        raise RuntimeError("file khong co luong video (video stream): %s" % path)
    s = j["streams"][0]
    num, den = s["r_frame_rate"].split("/")
    fps = float(num) / float(den) if float(den) else 0.0
    if fps <= 0:
        raise RuntimeError("fps doc duoc = 0, video loi: %s" % path)
    dur = float(j.get("format", {}).get("duration") or 0.0)
    nb = s.get("nb_frames")
    try:
        nb = int(nb)
    except (TypeError, ValueError):
        nb = int(round(dur * fps))
    return {"path": path, "w": int(s["width"]), "h": int(s["height"]),
            "fps": fps, "dur": dur, "nb_frames": nb,
            "codec": s.get("codec_name", "?")}


def has_audio(path):
    p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0",
                        "-show_entries", "stream=codec_name", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return bool((p.stdout or "").strip())


def det_scale(w, h):
    """Ti le thu nho de canh dai = 640, kem be ngang/cao sau khi thu nho."""
    scale = IN_SIZE / float(max(w, h))
    return scale, int(round(w * scale)), int(round(h * scale))


def stream_samples(path, step, sw, sh):
    """Lay mau video moi <step> giay. Tra (chi_so_mau, anh RGB sh x sw x 3).

    Dung fps=1/step nhu facetrack.py da kiem - moc thoi gian = i*step.
    """
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-vf",
           "fps=1/%.6f,scale=%d:%d" % (step, sw, sh),
           "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    # stderr phai di ra FILE, khong phai PIPE: pipe khong duoc doc se day day
    # bo dem va lam ffmpeg treo giua duong -> track bi cat ngan am tham.
    err = tempfile.TemporaryFile()
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=err, bufsize=10 ** 8)
    fsz = sw * sh * 3
    i = 0
    try:
        while True:
            buf = p.stdout.read(fsz)
            if len(buf) < fsz:
                break
            yield i, np.frombuffer(buf, np.uint8).reshape(sh, sw, 3)
            i += 1
    finally:
        try:
            p.stdout.close()
        except Exception:
            pass
        p.wait()
        if p.returncode not in (0, None):
            err.seek(0)
            msg = err.read().decode("utf-8", "replace").strip()[:400]
            err.close()
            die("ffmpeg loi khi lay mau video (ma loi %s):\n     %s"
                % (p.returncode, msg))
        err.close()


def frames_at_indices(path, idxs, sw, sh):
    """Lay dung nhung frame co CHI SO trong idxs, THEO THU TU TANG.

    KHONG dung -ss (hop dong muc 6: -ss co the nhay sai frame). Dung
    select=eq(n\\,N)+... nen chi giai ma MOT lan cho ca danh sach.
    """
    idxs = sorted(set(int(i) for i in idxs))
    if not idxs:
        return []
    expr = "+".join("eq(n\\,%d)" % i for i in idxs)
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-vf",
           "select='%s',scale=%d:%d" % (expr, sw, sh),
           "-vsync", "0", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    p = subprocess.run(cmd, capture_output=True)
    fsz = sw * sh * 3
    got = len(p.stdout) // fsz
    out = []
    for k in range(got):
        chunk = p.stdout[k * fsz:(k + 1) * fsz]
        out.append((idxs[k] if k < len(idxs) else -1,
                    np.frombuffer(chunk, np.uint8).reshape(sh, sw, 3)))
    return out


# ------------------------------------------------------------- tim file model
def find_model(resources=None):
    """Thu tu uu tien theo hop dong muc 4.3:
      1. --resources cua nguoi dung (tim de quy, uu tien <resources>/models/)
      2. assets/det_10g.onnx kem san trong skill
      3. bien moi truong FACE_MODEL_ONNX
      4. ~/.insightface/models/buffalo_l/det_10g.onnx tren may
    Tra (duong_dan, nhan_nguon, danh_sach_da_thu). duong_dan=None neu khong co.
    """
    tried = []
    if resources:
        cand = os.path.join(resources, "models", MODEL_NAME)
        tried.append(cand)
        if os.path.isfile(cand):
            return cand, "--resources (models/)", tried
        found = None
        if os.path.isdir(resources):
            for root, _dirs, files in os.walk(resources):
                if MODEL_NAME in files:
                    found = os.path.join(root, MODEL_NAME)
                    break
        tried.append(os.path.join(resources, "** (tim de quy)"))
        if found:
            return found, "--resources (tim de quy)", tried

    tried.append(BUNDLED_MODEL)
    if os.path.isfile(BUNDLED_MODEL):
        return BUNDLED_MODEL, "assets/ kem san trong skill", tried

    env = os.environ.get("FACE_MODEL_ONNX")
    if env:
        tried.append("$FACE_MODEL_ONNX = %s" % env)
        if os.path.isfile(env):
            return env, "bien moi truong FACE_MODEL_ONNX", tried

    tried.append(HOME_MODEL)
    if os.path.isfile(HOME_MODEL):
        return HOME_MODEL, "~/.insightface/models/buffalo_l/", tried

    return None, None, tried


# -------------------------------------------------------------------- decode
def _anchor_centers(stride):
    n = IN_SIZE // stride
    yy, xx = np.mgrid[:n, :n]
    c = np.stack([xx, yy], -1).astype(np.float32) * stride
    return np.repeat(c.reshape(-1, 2), NUM_ANCHORS, axis=0)


_CENTERS = {}          # dung LAZY: neu tinh o day thi thieu numpy la crash ngay


def _centers(stride):
    if stride not in _CENTERS:
        _CENTERS[stride] = _anchor_centers(stride)
    return _CENTERS[stride]


def _nms(boxes, scores, thr=NMS_THR):
    idx = scores.argsort()[::-1]
    keep = []
    while len(idx):
        i = idx[0]
        keep.append(i)
        if len(idx) == 1:
            break
        x1 = np.maximum(boxes[i, 0], boxes[idx[1:], 0])
        y1 = np.maximum(boxes[i, 1], boxes[idx[1:], 1])
        x2 = np.minimum(boxes[i, 2], boxes[idx[1:], 2])
        y2 = np.minimum(boxes[i, 3], boxes[idx[1:], 3])
        inter = np.maximum(0, x2 - x1) * np.maximum(0, y2 - y1)
        a1 = (boxes[i, 2] - boxes[i, 0]) * (boxes[i, 3] - boxes[i, 1])
        a2 = ((boxes[idx[1:], 2] - boxes[idx[1:], 0]) *
              (boxes[idx[1:], 3] - boxes[idx[1:], 1]))
        idx = idx[1:][inter / (a1 + a2 - inter + 1e-9) <= thr]
    return keep


class Detector(object):
    """SCRFD/RetinaFace det_10g.onnx qua onnxruntime (CPU).

    KHONG dung mask mau da: mask da bat ca tay, co, va vung mau be tren
    screen-record -> da cho ket qua sai.
    """

    def __init__(self, model_path, thr=DEFAULT_THR):
        require_numpy()
        require_onnxruntime()
        import onnxruntime as ort
        if not os.path.isfile(model_path):
            die("khong thay file model: %s" % model_path)
        try:
            self.sess = ort.InferenceSession(
                model_path, providers=["CPUExecutionProvider"])
        except Exception as exc:
            die("khong nap duoc model %s (%s)" % (model_path, exc))
        self.iname = self.sess.get_inputs()[0].name
        self.onames = [o.name for o in self.sess.get_outputs()]
        self.thr = float(thr)

    def __call__(self, img, sw, sh, scale):
        """img: sh x sw x 3 RGB da thu nho. Tra list (box, score) theo TOA DO GOC,
        sap xep dien tich giam dan."""
        pad = np.zeros((IN_SIZE, IN_SIZE, 3), np.uint8)
        pad[:sh, :sw] = img
        blob = ((pad.astype(np.float32) - 127.5) / 128.0).transpose(2, 0, 1)[None]
        out = dict(zip(self.onames, self.sess.run(None, {self.iname: blob})))
        s_keys = sorted([n for n in self.onames if out[n].shape[1] == 1],
                        key=lambda n: -out[n].shape[0])
        b_keys = sorted([n for n in self.onames if out[n].shape[1] == 4],
                        key=lambda n: -out[n].shape[0])
        boxes, scores = [], []
        for stride, sk, bk in zip(STRIDES, s_keys, b_keys):
            sc = out[sk].ravel()
            dist = out[bk] * stride
            cen = _centers(stride)
            m = sc >= self.thr
            if not m.any():
                continue
            cc, dd = cen[m], dist[m]
            boxes.append(np.stack([cc[:, 0] - dd[:, 0], cc[:, 1] - dd[:, 1],
                                   cc[:, 0] + dd[:, 2], cc[:, 1] + dd[:, 3]], -1))
            scores.append(sc[m])
        if not boxes:
            return []
        boxes = np.concatenate(boxes) / scale
        scores = np.concatenate(scores)
        res = [([float(v) for v in boxes[i]], float(scores[i]))
               for i in _nms(boxes, scores)]
        res.sort(key=lambda d: -box_area(d[0]))
        return res


# ------------------------------------------------------------ hinh hoc hop mat
def box_area(b):
    return max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])


def box_center(b):
    return ((b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0)


def box_round(b):
    return [int(round(v)) for v in b]


def box_union(boxes):
    a = np.array(boxes, float)
    return [float(a[:, 0].min()), float(a[:, 1].min()),
            float(a[:, 2].max()), float(a[:, 3].max())]


def box_inside(b, w, h):
    return b[0] >= 0 and b[1] >= 0 and b[2] <= w and b[3] <= h


def dist(p, q):
    return ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) ** 0.5


def select_track(cands_per_sample, max_jump, confirm=2, size_ratio=3.0):
    """LUAT CHON KHI CO NHIEU MAT (xem references/nhieu-mat-va-drift.md).

    Do that: mot doan screen-record chua anh contact-sheet mat cua chinh dien gia
    da cho toi 11 detection trong 1 frame. 'Lay hop lon nhat' don doc la MONG
    o cho do - khi mat that bi khuat, o anh to nhat trong contact sheet thang,
    va tam zoom nhay sang mot o anh.

    Luat (chay 2 luot tren TOAN BO danh sach, khong phai 1 luot online):
      1. mau dau tien co mat            -> lay hop LON NHAT
      2. mau sau do                     -> chi xet ung vien cach tam truoc
                                           <= max_jump, trong so do lay LON NHAT
      3. khong ung vien nao trong ban kinh -> chua nhan ngay, giu lam 'cho xac
         nhan'. Chi nhan ung vien co CO tuong duong mat cu (ti le dien tich
         trong 1/size_ratio .. size_ratio). Neu mau ke tiep cung nhay ve GAN
         cho moi do (<= max_jump) thi day la CAT CANH / dien gia doi cho THAT
         -> nhan HOI TO ca cac mau dang cho, khong mat mau nao. Neu khong duoc
         xac nhan trong <confirm> mau thi day la mot lan bat lac -> tu choi that.

    Loc theo CO mat la cai chan quan trong: o anh trong contact sheet 4x4 co
    dien tich chi 1/16 mat that (ti le 0.06, ngoai nguong 1/3) -> khong bao gio
    duoc nhan. Con cat canh THAT tu canh rong sang canh gan da do duoc ti le
    0.42 -> vao nguong, van nhan binh thuong.

    Vi sao phai nhan hoi to: neu tu choi thang, doan sau cat canh se mat 1-2 mau
    DO DUOC. Da gap that: bo 2 mau lam hop mat gop tut tu x=955 xuong x=844,
    tuc bao safe zone NHO HON su that 111 px - dung dung cai loi da phai tra gia.

    cands_per_sample: list, moi phan tu la list (box, score) da sap theo dien tich.
    Tra list cung do dai: (box|None, score, nhan).
    """
    n = len(cands_per_sample)
    picks = [(None, 0.0, "khong-co-mat")] * n
    prev_box = None
    pending = []          # [(i, box, score)] cac mau nhay xa dang cho xac nhan
    confirm = max(1, int(confirm))
    r = max(1.0001, float(size_ratio))
    for i, cands in enumerate(cands_per_sample):
        if not cands:
            picks[i] = (None, 0.0, "khong-co-mat")
            pending = []
            continue
        if prev_box is None:
            b, s = max(cands, key=lambda d: box_area(d[0]))
            picks[i] = (b, s, "lon-nhat")
            prev_box = b
            pending = []
            continue
        prev = box_center(prev_box)
        near = [d for d in cands if dist(box_center(d[0]), prev) <= max_jump]
        if near:
            b, s = max(near, key=lambda d: box_area(d[0]))
            picks[i] = (b, s, "lon-nhat-trong-ban-kinh")
            prev_box = b
            pending = []
            continue
        # nhay xa: chi xet ung vien co CO tuong duong mat dang bam
        a_prev = max(1.0, box_area(prev_box))
        same_size = [d for d in cands
                     if (1.0 / r) <= (box_area(d[0]) / a_prev) <= r]
        if not same_size:
            picks[i] = (None, 0.0, "tu-choi-nhay-xa-co-khac-han")
            pending = []
            continue
        b, s = max(same_size, key=lambda d: box_area(d[0]))
        if pending and dist(box_center(b), box_center(pending[-1][1])) <= max_jump:
            pending.append((i, b, s))
        else:
            pending = [(i, b, s)]
        if len(pending) >= confirm:
            nhan = "nhay-xa-da-xac-nhan-%d-mau" % len(pending)
            for j, bb, ss in pending:
                picks[j] = (bb, ss, nhan)
            prev_box = pending[-1][1]
            pending = []
        else:
            picks[i] = (None, 0.0, "tu-choi-nhay-xa-cho-xac-nhan")
    return picks


# ------------------------------------------------- doc track da luu, tra hop mat
def track_face_at(track, t, field="box"):
    """Hop mat tai thoi diem t giay, lay tu track da luu.

    field="box"      -> hop dieu khien zoom (da va lo hong + lam min)
    field="box_det"  -> CHI hop do duoc that (dung cho safe zone / verify)

    Uu tien: mau gan nhat co hop -> noi suy tuyen tinh giua 2 mau bao quanh ->
    hop gan nhat. Tra (box, nhan_nguon).
    """
    rows = [{"t": s["t"], "box": s[field]}
            for s in track["samples"] if s.get(field)]
    if not rows:
        return None, "khong-co-mau-nao-co-mat"
    exact = min(rows, key=lambda s: abs(s["t"] - t))
    step = float(track.get("step", 1.0))
    if abs(exact["t"] - t) <= step / 2.0 + 1e-6:
        return list(exact["box"]), "mau t=%.2fs" % exact["t"]
    before = [s for s in rows if s["t"] <= t]
    after = [s for s in rows if s["t"] >= t]
    if before and after:
        a, b = before[-1], after[0]
        if b["t"] - a["t"] < 1e-9:
            return list(a["box"]), "mau t=%.2fs" % a["t"]
        r = (t - a["t"]) / (b["t"] - a["t"])
        box = [a["box"][i] + (b["box"][i] - a["box"][i]) * r for i in range(4)]
        return box, "noi suy %.2fs..%.2fs" % (a["t"], b["t"])
    return list(exact["box"]), "mau gan nhat t=%.2fs" % exact["t"]


def measured_boxes_in(track, t0, t1):
    """Cac hop DO DUOC (box_det) co moc thoi gian trong [t0, t1]."""
    return [s for s in track["samples"]
            if s.get("box_det") and t0 - 1e-9 <= s["t"] <= t1 + 1e-9]


def nearest_measured_age(track, t):
    """Khoang cach (giay) tu t den mau DO DUOC gan nhat. None neu khong co mau nao."""
    rows = [s["t"] for s in track["samples"] if s.get("box_det")]
    if not rows:
        return None
    return min(abs(x - t) for x in rows)


def median_box(rows):
    a = np.array([s["box"] for s in rows if s.get("box")], float)
    if not len(a):
        return None
    return [float(np.median(a[:, i])) for i in range(4)]


# ------------------------------------------- tinh khung crop, KHONG BAO GIO cat mat
def solve_window(zoom_req, face, w, h, margin, desired=None):
    """Chon zoom + tam crop sao cho: (a) khung crop nam trong khung hinh,
    (b) hop mat NAM TRON trong khung crop, cach vien >= margin px.

    face    : hop mat PHAI om tron (nen dua hop GOP ca doan punch, khong phai
              hop cua 1 frame - neu khong thi dau/cuoi doan mat co the loi ra).
    desired : tam muon ngam vao (mac dinh: tam cua face). Se bi keo lai neu
              lam mat loi ra khoi khung crop.

    Toan: o muc zoom z, khung crop rong w/z, cao h/z.
      - can w/z >= (be ngang mat + 2*margin)  -> z <= w / (fw + 2*margin)
      - tuong tu cho chieu cao
    Ngoai ra khung crop phai truot duoc de om mat: crop_x thuoc doan
      [max(0, fx2+margin-w/z), min(w-w/z, fx1-margin)]
    Neu doan do rong (mat sat vien khung), margin bi ep nho lai theo vien.

    Tra dict: zoom thuc dung, tam (cx,cy), khung crop tai dinh zoom, co bi ha
    zoom khong va vi sao.
    """
    fx1, fy1, fx2, fy2 = face
    fw, fh = max(1.0, fx2 - fx1), max(1.0, fy2 - fy1)
    # margin khong duoc lon hon khoang trong that co giua mat va vien khung
    mx = max(0.0, min(margin, fx1, w - fx2))
    my = max(0.0, min(margin, fy1, h - fy2))
    z_max_x = w / (fw + 2.0 * mx) if (fw + 2.0 * mx) > 0 else 99.0
    z_max_y = h / (fh + 2.0 * my) if (fh + 2.0 * my) > 0 else 99.0
    z_cap = max(1.0, min(z_max_x, z_max_y))
    zoom = float(zoom_req)
    capped = False
    if zoom > z_cap:
        zoom, capped = z_cap, True
    if zoom < 1.0:
        zoom = 1.0
    cw, ch = w / zoom, h / zoom
    fcx, fcy = box_center(face) if desired is None else (desired[0], desired[1])

    def clamp_axis(desired_lo, span, f_lo, f_hi, m, limit):
        lo = max(0.0, f_hi + m - span)
        hi = min(limit - span, f_lo - m)
        if lo > hi:                       # khong the giu ca margin -> bo margin
            lo = max(0.0, f_hi - span)
            hi = min(limit - span, f_lo)
        if lo > hi:                       # van khong duoc -> giu giua mat
            return max(0.0, min(limit - span, (f_lo + f_hi) / 2.0 - span / 2.0))
        return max(lo, min(hi, desired_lo))

    cx0 = clamp_axis(fcx - cw / 2.0, cw, fx1, fx2, mx, w)
    cy0 = clamp_axis(fcy - ch / 2.0, ch, fy1, fy2, my, h)
    return {"zoom": round(zoom, 4), "zoom_req": round(float(zoom_req), 4),
            "zoom_capped": capped, "zoom_cap": round(z_cap, 4),
            "cx": round(cx0 + cw / 2.0, 2), "cy": round(cy0 + ch / 2.0, 2),
            "crop": [round(cx0, 1), round(cy0, 1), round(cw, 1), round(ch, 1)],
            "margin_x": round(mx, 1), "margin_y": round(my, 1)}


def out_center(face_center, crop, zoom):
    """Tam mat SE nam o dau trong khung ket qua (pixel, toa do khung ra)."""
    return ((face_center[0] - crop[0]) * zoom, (face_center[1] - crop[1]) * zoom)


def zoom_to_center(fcx, fcy, w, h, band):
    """Zoom TOI THIEU de keo tam mat vao dai giua khung.

    band = ti le be rong dai giua duoc chap nhan (0.30 = 30% giua khung, tuc
    lech toi da 15% moi ben).

    TOAN HOC - day la cho de hieu sai nhat ca skill:
    o muc zoom z, khung crop rong w/z va chi truot duoc trong [0, w - w/z].
    Nghia la tam nhin chi doi duoc toi da (1 - 1/z)/2 be ngang khung.
    Voi z = 1.12 con so do la 5.4%. Mot cai mat nam o 78% chieu cao khung
    (rat thuong gap o video doc 9:16: nguoi ngoi thap, chua cho cho caption)
    KHONG THE nao keo ve giua bang zoom 1.12 - khong phai loi code, la hinh hoc.

    Goi d = khoang cach tu tam mat den vien GAN nhat. Muon tam mat cach tam
    khung khong qua b = band/2 * canh, can:
        z >= (canh/2 - b) / d
    Tra z can thiet (>= 1.0).
    """
    bx = (band / 2.0) * w
    by = (band / 2.0) * h
    dx = max(1.0, min(fcx, w - fcx))
    dy = max(1.0, min(fcy, h - fcy))
    zx = (w / 2.0 - bx) / dx
    zy = (h / 2.0 - by) / dy
    return max(1.0, zx, zy)


def frame_of(t, fps, nb_frames=None):
    n = int(round(t * fps))
    if nb_frames is not None:
        n = max(0, min(nb_frames - 1, n))
    return max(0, n)
