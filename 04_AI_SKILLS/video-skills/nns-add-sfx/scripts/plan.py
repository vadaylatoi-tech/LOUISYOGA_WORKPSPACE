# -*- coding: utf-8 -*-
"""plan.py - lap CUE SHEET (danh sach hieu ung + moc thoi gian).

MAT DINH LA HOOK-WEIGHTED (don vao dau video).
Ly do that: creator nay da xem mot ban 53 cue rai deu ca video roi tu tay cat
lai chi con ~20 giay dau. Nen mac dinh:
   - trong hook (0 .. --hook-len, mac dinh 20s hoac ca video neu video <= 30s):
     dat cue day theo --density (mac dinh 0.8 cue/giay)
   - sau hook: CHI dat cue o cho hinh THAT SU doi (cat canh do bang scene
     detection cua ffmpeg), khong tu them gi nua

Co the ghi de hoan toan bang --cues <json> (caller tu cho moc chinh xac).

  python scripts/plan.py --video "<video>" --out sfx_cues.json \
      --onsets sfx_onsets.json [--resources "<dir>"] [--max-t 20] [--dry-run]
"""
from __future__ import print_function

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

C.setup_stdout()

PLAN_VERSION = 2

# vong quay vai cho cac nhip trong hook (bat dau bang cu danh manh)
ROT_PHRASE = ["impact", "confirm", "impact", "transition"]
ROT_ACCENT = ["accent", "transition", "accent", "accent", "negative", "accent"]


# --------------------------------------------------------------- phat hien cat

def detect_cuts(video, thr):
    """Tim cat canh cung bang scene detection cua ffmpeg. Tra ve list giay."""
    p = C.run(["ffmpeg", "-hide_banner", "-v", "error", "-nostats", "-i", video,
               "-filter_complex",
               "select='gt(scene,%.3f)',metadata=print:file=-" % thr,
               "-an", "-f", "null", "-"],
              what="scene detection that bai tren video nay")
    txt = p.stdout.decode("utf-8", "replace")
    out = []
    for m in re.finditer(r"pts_time:([0-9.]+)", txt):
        t = float(m.group(1))
        if t >= 0.40 and (not out or t - out[-1] >= 0.30):
            out.append(round(t, 3))
    return out


# ------------------------------------------------------------- nhip cua loi noi

def detect_beats(video):
    """Tim nhip trong loi noi tu chinh nang luong cua file nay.

    KHONG ghim nguong dB co dinh: suy ra tu phan bo (p1 = san on, p70 = muc noi),
    dung dung ly do da ghi trong hop dong muc 5.
    """
    import numpy as np
    x = C.decode_audio(video, channels=1)
    if len(x) == 0:
        C.die("khong doc duoc audio cua video: %s" % video)
    e = C.env_db(x.astype(np.float64), C.HOP_SPEECH)
    n = len(e)
    if n < 10:
        return [], [], {}
    p1 = float(np.percentile(e, 1))
    p50 = float(np.percentile(e, 50))
    p70 = float(np.percentile(e, 70))
    speech_thr = p70 - 12.0            # duoi nguong nay coi la khoang nghi
    above = e > speech_thr

    gap = int(round(0.22 / C.HOP_SPEECH))
    phrase = []
    for i in range(1, n):
        if above[i] and not above[i - 1]:
            lo = max(0, i - gap)
            if not above[lo:i].any():
                phrase.append(round(i * C.HOP_SPEECH, 3))

    k = max(1, int(round(0.06 / C.HOP_SPEECH)))
    sm = np.convolve(e, np.ones(k) / k, mode="same")
    acc_thr = p70 - 3.0
    accent = []
    last = -9.0
    for i in range(2, n - 2):
        t = i * C.HOP_SPEECH
        if sm[i] >= sm[i - 1] and sm[i] > sm[i + 1] and sm[i] > acc_thr \
                and t - last > 0.45:
            accent.append(round(t, 3))
            last = t

    strength = {}
    for t in phrase + accent:
        i = min(n - 1, int(round(t / C.HOP_SPEECH)))
        strength[t] = float(sm[i])
    return phrase, accent, {"p1": p1, "p50": p50, "p70": p70,
                            "speech_thr": speech_thr, "acc_thr": acc_thr,
                            "strength": strength, "dur": len(x) / float(C.SR)}


# ------------------------------------------------------- chon file cho tung vai

class Picker(object):
    """Chon file SFX cho mot vai, quay vong, khong lap lai trong 3 cue gan nhat."""

    def __init__(self, table):
        self.by_role = {}
        for k, v in sorted(table.items()):
            if not v.get("usable"):
                continue
            self.by_role.setdefault(v.get("role", "other"), []).append((k, v))
        for role in self.by_role:
            # uu tien: dung ten quen thuoc truoc, roi file ngan truoc
            self.by_role[role].sort(
                key=lambda kv, r=role: (C.prefer_rank(r, kv[0]),
                                        kv[1]["rec_dur"] > 1.2, kv[0]))
        self.idx = {}
        self.recent = []

    def has(self, role):
        return bool(self.by_role.get(role))

    def pick_cut(self):
        """Cat canh thi LUON dung whoosh/swoosh - quay vong trong 3 file tot nhat."""
        pool = [kv for kv in self.by_role.get("transition", [])
                if C.prefer_rank("transition", kv[0]) <= 2][:3]
        if not pool:
            return self.pick("transition")
        i = self.idx.get("_cut", 0)
        self.idx["_cut"] = i + 1
        k, v = pool[i % len(pool)]
        return k, v, "transition"

    def pick(self, role):
        pool = self.by_role.get(role)
        if not pool:
            for alt in ("accent", "transition", "impact", "confirm", "other"):
                pool = self.by_role.get(alt)
                if pool:
                    role = alt
                    break
        if not pool:
            return None, None, None
        i = self.idx.get(role, 0)
        for _ in range(len(pool)):
            k, v = pool[i % len(pool)]
            i += 1
            if k not in self.recent[-3:]:
                self.idx[role] = i
                self.recent.append(k)
                return k, v, role
        k, v = pool[self.idx.get(role, 0) % len(pool)]
        self.idx[role] = self.idx.get(role, 0) + 1
        self.recent.append(k)
        return k, v, role


def make_cue(name, info, role, t, why, dur=None, gain_db=None, max_dur=None):
    align = info.get("rec_align", "start")
    rec = float(info["rec_dur"])
    d = float(dur) if dur is not None else rec
    cap = max_dur if max_dur is not None else C.ROLE_MAX_DUR.get(
        role, C.ROLE_MAX_DUR["other"])
    if dur is None and cap:
        d = min(d, cap)
    d = max(0.05, d)
    offset = float(info["onset"])
    if align == "end" and d < rec:
        # CAT TU DAU, giu doan ket: riser van len tot va DINH van dung dung cho
        offset = max(0.0, offset + (rec - d))
    if role == "bed":
        fin, fout = 0.15, min(0.60, d * 0.35)
    elif align == "end":
        fin, fout = min(0.20, d * 0.25), 0.02
    else:
        fin, fout = 0.0, min(0.08, max(0.02, d * 0.2))
    if gain_db is None:
        target = C.ROLE_TARGET_PEAK.get(role, C.ROLE_TARGET_PEAK["other"])
        g = target - float(info.get("seg_peak_dbfs", -12.0))
        gain_db = max(-40.0, min(12.0, g))
    return {
        "t": round(float(t), 3),
        "file": name,
        "role": role,
        "align": align,
        "offset": round(offset, 3),
        "dur": round(d, 3),
        "gain_db": round(float(gain_db), 1),
        "fade_in": round(fin, 3),
        "fade_out": round(fout, 3),
        "why": why,
    }


# ------------------------------------------------------------------ cues tu file

def resolve_manual(items, table, picker):
    """Nhan cue do caller cho san, dien not cac truong con thieu tu bang onset."""
    by_base = {}
    for k in table:
        by_base.setdefault(os.path.basename(k).lower(), k)
        by_base.setdefault(k.lower(), k)
    out = []
    for i, it in enumerate(items):
        if not isinstance(it, dict) or "t" not in it:
            C.die("cue thu %d trong --cues khong hop le: can it nhat truong \"t\".\n"
                  "Dinh dang: {\"t\": 3.20, \"file\": \"pop.mp3\", \"gain_db\": -14}"
                  % (i + 1))
        want = str(it.get("file") or "").strip()
        if want:
            k = by_base.get(want.lower()) or by_base.get(C.disp(want).lower())
            if not k:
                near = [b for b in sorted(by_base)
                        if want.lower().split(".")[0][:5] in b][:6]
                C.die("cue thu %d: khong co file \"%s\" trong thu vien SFX.\n"
                      "Gan giong: %s\n"
                      "Xem het ten bang: python scripts/probe.py --show 0 ..."
                      % (i + 1, want, ", ".join(near) or "(khong co)"))
            info = table[k]
            if not info.get("usable"):
                C.die("cue thu %d: file \"%s\" khong dung duoc (%s)."
                      % (i + 1, want, info.get("reason", "?")))
            role = it.get("role") or info.get("role", "other")
        else:
            role = it.get("role") or "accent"
            k, info, role = picker.pick(role)
            if k is None:
                C.die("cue thu %d: khong co file nao cho vai \"%s\"." % (i + 1, role))
        cue = make_cue(k, info, role, it["t"], it.get("why", "cue do caller cho"),
                       dur=it.get("dur"), gain_db=it.get("gain_db"))
        for f in ("offset", "fade_in", "fade_out", "align"):
            if f in it and it[f] is not None:
                cue[f] = it[f] if f == "align" else round(float(it[f]), 3)
        out.append(cue)
    return out


# ------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Lap cue sheet SFX")
    C.add_common_args(ap, need_out=True)
    ap.add_argument("--onsets", default=None,
                    help="file JSON tu probe.py (mac dinh: sfx_onsets.json canh --out)")
    ap.add_argument("--cues", default=None,
                    help="JSON cue do caller cho san (ghi de toan bo phan tu dong)")
    ap.add_argument("--max-t", type=float, default=None,
                    help="chi giu cue trong N giay dau")
    ap.add_argument("--hook-len", type=float, default=None,
                    help="do dai hook (mac dinh: ca video neu <=30s, con lai 20s)")
    ap.add_argument("--density", type=float, default=0.8,
                    help="so cue moi giay trong hook (mac dinh 0.8)")
    ap.add_argument("--risers", type=int, default=2,
                    help="so riser dat trong hook (mac dinh 2)")
    ap.add_argument("--scene", type=float, default=0.35,
                    help="nguong scene detection (mac dinh 0.35)")
    ap.add_argument("--target", type=float, default=-14.0)
    ap.add_argument("--tp", type=float, default=-1.5)
    a = ap.parse_args()
    C.require_numpy(a.video)

    if not os.path.isfile(a.video):
        C.die("khong tim thay video: %s" % a.video)

    # Nguoi dung dua --resources thi phai dung dung do, khong am tham doi nguon.
    res_prob = C.resources_problem(a.resources)
    if res_prob:
        head, lines = C.resources_guidance(res_prob[0], res_prob[1])
        C.die_block(head, lines,
                    "python scripts/preflight.py --video \"%s\"" % a.video)

    onsets_path = a.onsets or os.path.join(
        os.path.dirname(os.path.abspath(a.out)) or ".", "sfx_onsets.json")
    if not os.path.isfile(onsets_path):
        C.die("khong tim thay bang onset: %s\n"
              "Chay buoc probe truoc:\n"
              "    python scripts/probe.py --video \"%s\" --out \"%s\"%s"
              % (C.disp(onsets_path), a.video, C.disp(onsets_path),
                 (" --resources \"%s\"" % a.resources) if a.resources else ""))
    ons = C.read_json(onsets_path)
    table = ons.get("files") or {}
    if not table:
        C.die("bang onset rong: %s. Chay lai probe.py." % C.disp(onsets_path))

    sfx_dir = ons.get("sfx_dir")
    if a.resources:
        d2, files2, _src, _n = C.find_sfx_library(a.resources)
        if d2:
            sfx_dir = C.disp(d2)
    if not sfx_dir or not os.path.isdir(sfx_dir):
        C.die("thu muc SFX trong bang onset khong con ton tai: %s\n"
              "Chay lai probe.py voi --resources dung." % C.disp(sfx_dir))
    # Bang onset phai khop thu muc dang dung. Chi giu file CO THAT o do -
    # neu khong, plan se chon file khong ton tai va apply moi chet.
    n_all = len(table)
    table = {k: v for k, v in table.items()
             if os.path.isfile(os.path.join(sfx_dir, k.replace("/", os.sep)))}
    n_drop = n_all - len(table)
    if not table:
        C.die("bang onset khong khop thu muc SFX dang dung.\n"
              "Bang onset ghi %d file, nhung khong file nao ton tai trong:\n"
              "    %s\n"
              "Ban da doi thu vien SFX giua probe.py va plan.py.\n"
              "Chay lai probe.py voi dung --resources nay:\n"
              "    python scripts/probe.py --video \"%s\" --out \"%s\"%s"
              % (n_all, C.disp(sfx_dir), a.video, C.disp(onsets_path),
                 (" --resources \"%s\"" % a.resources) if a.resources else ""))

    vid = C.probe_media(a.video)
    if not vid["has_audio"]:
        C.die("video khong co tieng goc. Chay preflight de xem huong dan.")
    dur = vid["duration"]

    hook = a.hook_len if a.hook_len is not None else (dur if dur <= 30.0 else 20.0)
    hook = max(0.5, min(hook, dur))

    print("")
    print("  nns-add-sfx / PLAN")
    print("  video    : %s  %.2fs %.3ffps" % (C.disp(a.video), dur, vid["fps"]))
    print("  SFX      : %s (%d file trong bang onset%s)"
          % (C.disp(sfx_dir), len(table),
             ", bo %d file khong co trong thu muc nay" % n_drop if n_drop else ""))

    picker = Picker(table)
    cuts = detect_cuts(a.video, a.scene)
    print("  cat canh : %d cho %s" % (len(cuts), [round(c, 2) for c in cuts[:12]]))

    if a.cues:
        if not os.path.isfile(a.cues):
            C.die("khong tim thay file --cues: %s" % a.cues)
        raw = C.read_json(a.cues)
        items = raw.get("cues") if isinstance(raw, dict) else raw
        if not isinstance(items, list):
            C.die("--cues phai la mang JSON, hoac object co truong \"cues\".")
        cues = resolve_manual(items, table, picker)
        mode = "cues do caller cho (%d cue)" % len(cues)
        stats = {}
    else:
        phrase, accent, stats = detect_beats(a.video)
        print("  nhip noi : %d dau cau, %d trong am (nguong noi %.1f dB tu p70=%.1f)"
              % (len(phrase), len(accent), stats["speech_thr"], stats["p70"]))

        min_gap = 1.0 / max(0.05, a.density)
        chosen = []  # (t, kind)
        for t in cuts:
            chosen.append((t, "cut"))

        def free(t):
            for tt, kind in chosen:
                if kind != "cut" and abs(tt - t) < min_gap:
                    return False
                if kind == "cut" and abs(tt - t) < 0.25:
                    return False
            return True

        if not phrase and not accent:
            print("  luu y    : khong tim ra nhip noi nao -> chi dat cue o cat canh")
        for t in sorted(phrase):
            if t < hook and free(t):
                chosen.append((t, "phrase"))
        for t in sorted(accent):
            if t < hook and free(t):
                chosen.append((t, "accent"))
        chosen.sort(key=lambda x: x[0])

        cues = []
        i_ph = i_ac = 0
        for t, kind in chosen:
            if kind == "cut":
                role = "transition"
                why = "cat canh %.2fs" % t
            elif kind == "phrase":
                role = ROT_PHRASE[i_ph % len(ROT_PHRASE)]
                i_ph += 1
                why = "dau cau trong hook"
            else:
                role = ROT_ACCENT[i_ac % len(ROT_ACCENT)]
                i_ac += 1
                why = "trong am trong hook"
            if t < 0.30 and not cues:
                role = "impact"
                why = "cu danh mo dau"
            if kind == "cut":
                k, info, role = picker.pick_cut()
            else:
                k, info, role = picker.pick(role)
            if k is None:
                C.die("thu vien SFX khong co file nao dung duoc cho vai %s." % role)
            cues.append(make_cue(k, info, role, t, why))

        # rieng riser: dat sao cho DINH cua no roi dung vao nhip manh nhat
        if a.risers > 0 and picker.has("riser"):
            st = stats.get("strength", {})
            cand = sorted([(st.get(t, -99.0), t) for t, kind in chosen
                           if kind in ("phrase", "cut") and t > 1.0], reverse=True)
            placed = 0
            used = []
            for _s, t in cand:
                if placed >= a.risers:
                    break
                if any(abs(t - u) < 4.0 for u in used):
                    continue
                k, info, role = picker.pick("riser")
                if k is None:
                    break
                cue = make_cue(k, info, "riser", t,
                               "riser leo len, DINH dung %.2fs" % t)
                if cue["t"] - cue["dur"] < 0.0:
                    continue
                cues.append(cue)
                used.append(t)
                placed += 1
        cues.sort(key=lambda c: (c["t"], c["file"]))
        mode = ("hook-weighted: %.1fs hook @ %.2f cue/giay, sau hook chi cat canh"
                % (hook, a.density))

    if a.max_t is not None:
        before = len(cues)
        cues = [c for c in cues if c["t"] <= a.max_t + 1e-6]
        print("  --max-t  : giu %d/%d cue trong %.2fs dau"
              % (len(cues), before, a.max_t))

    # bo cue vuot qua het video
    keep = []
    for c in cues:
        start = c["t"] - c["dur"] if c["align"] == "end" else c["t"]
        if start >= dur - 0.02:
            continue
        if start < 0.0:
            c["dur"] = round(c["dur"] + start, 3)
            c["t"] = round(c["t"], 3)
            if c["dur"] < 0.05:
                continue
        keep.append(c)
    cues = keep

    if not cues:
        C.die("ke hoach ra 0 cue. Thu ha --density, tang --hook-len,\n"
              "hoac cho cue tay bang --cues.")

    obj = {
        "version": PLAN_VERSION,
        "video": C.disp(os.path.abspath(a.video)),
        "duration": round(dur, 6),
        "fps": round(vid["fps"], 6),
        "sr": C.SR,
        "sfx_dir": C.disp(sfx_dir),
        "onsets": C.disp(os.path.abspath(onsets_path)),
        "hook_len": round(hook, 3),
        "density": a.density,
        "mode": mode,
        "target_lufs": a.target,
        "target_tp": a.tp,
        "cues": cues,
    }

    # ------------------------------------------------------------------ in ra
    print("  che do   : %s" % mode)
    print("")
    print("  %-8s %-24s %-11s %8s %7s %7s  %s"
          % ("t", "file", "vai", "offset", "dur", "gain", "ly do"))
    print("  " + "-" * 96)
    for c in cues:
        print("  %-8.2f %-24s %-11s %8.3f %7.3f %+6.1f  %s%s"
              % (c["t"], c["file"][:24], c["role"], c["offset"], c["dur"],
                 c["gain_db"], c["why"], "  [ket thuc dung t]" if c["align"] == "end" else ""))
    n_hook = len([c for c in cues if c["t"] < hook])
    print("")
    print("  tong     : %d cue  |  trong hook %d (%.2f cue/giay)  |  sau hook %d"
          % (len(cues), n_hook, n_hook / hook if hook else 0.0, len(cues) - n_hook))

    if a.dry_run:
        print("  --dry-run: KHONG ghi file.")
        print("")
        return
    C.write_json(a.out, obj)
    print("  da ghi   : %s" % C.disp(a.out))
    print("")
    print("  Buoc tiep: python scripts/apply.py --video \"%s\" --out <ket-qua.mp4> "
          "--cues \"%s\"" % (a.video, C.disp(a.out)))
    print("")


if __name__ == "__main__":
    main()
