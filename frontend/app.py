import streamlit as st
import os
import pandas as pd
import requests
import json
import base64

st.set_page_config(
    page_title="FoodRescue AI",
    page_icon="🍳",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_DIR = os.path.join(
    BASE_DIR,
    "image"
)

TRANSLATION_DIR = os.path.join(
    BASE_DIR,
    "translation"
)

BACKEND_URL = os.environ.get(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)

MAX_IMAGES = 5

st.markdown(
    """
<style>

.stApp,
[data-testid="stAppViewContainer"] {
    background:
        linear-gradient(
            160deg,
            #020617 0%,
            #06283d 35%,
            #0e4a63 60%,
            #0a1a2e 85%,
            #020617 100%
        ) !important;

    overflow-x: hidden;
}

html, body {
    overflow-x: hidden;
}

[data-testid="stHeader"] {
    display: none !important;
}

.main {
    padding: 2rem 3rem;
}

.block-container,
[data-testid="stAppViewBlockContainer"] {
    padding-top: 1rem !important;
}

.stButton > button {
    background: linear-gradient(
        90deg,
        #06b6d4,
        #3b82f6
    );

    color: white;
    border-radius: 10px;
    border: none;

    padding: 0.6rem 1.2rem;

    font-weight: 600;

    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: scale(1.02);

    box-shadow:
        0 4px 16px
        rgba(6, 182, 212, 0.45);
}

div[data-testid="stMetric"] {
    background: #0d1b2a;

    border: 1px solid #1e3a56;

    border-radius: 12px;

    padding: 1rem;
}

.stRadio > label {
    font-weight: 600;
    color: #e5e7eb;
}

h1 {
    background:
        linear-gradient(
            90deg,
            #22d3ee,
            #3b82f6
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    font-weight: 800;
}

.navbar {
    position: relative;

    left: 50%;
    right: 50%;

    width: 100vw;

    margin-left: -50vw;
    margin-right: -50vw;

    display: flex;
    align-items: center;

    gap: 16px;

    background:
        rgba(13, 27, 42, 0.78);

    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);

    border-bottom:
        1px solid
        rgba(34, 211, 238, 0.18);

    border-radius: 0;

    padding: 0.85rem 3rem;

    margin-top: -2rem;
    margin-bottom: 4rem;

    box-shadow:
        0 8px 24px
        rgba(0, 0, 0, 0.35),

        inset 0 1px 0
        rgba(255, 255, 255, 0.04);
}

.navbar::after {
    content: "";

    position: absolute;

    left: 2rem;
    right: 2rem;

    bottom: 0;

    height: 2px;

    background:
        linear-gradient(
            90deg,
            #22d3ee,
            #3b82f6,
            transparent
        );

    opacity: 0.7;
}

.navbar-logo {
    width: 44px;
    height: 44px;

    object-fit: contain;

    flex-shrink: 0;

    filter:
        drop-shadow(
            0 2px 8px
            rgba(34, 211, 238, 0.35)
        );
}

.navbar-title {
    font-size: 1.25rem;

    font-weight: 800;

    background:
        linear-gradient(
            90deg,
            #f3f4f6,
            #cbd5e1
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    line-height: 1.2;
}

.navbar-tagline {
    font-size: 0.8rem;

    color: #7c93ad;

    font-weight: 500;

    margin-top: 2px;
}

.badge-pill {
    display: inline-block;

    background:
        rgba(34, 211, 238, 0.12);

    color: #22d3ee;

    border:
        1px solid
        rgba(34, 211, 238, 0.35);

    padding:
        0.35rem 1rem;

    border-radius: 999px;

    font-size: 0.85rem;

    font-weight: 600;

    margin-bottom: 1rem;
}

.hero-title {
    font-size: 3rem;

    font-weight: 800;

    line-height: 1.15;

    color: #f3f4f6;

    margin-bottom: 0.7rem;
}

.hero-title .highlight {
    background:
        linear-gradient(
            90deg,
            #22d3ee,
            #3b82f6
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    color: #93a3b8;

    font-size: 1.05rem;

    line-height: 1.6;

    max-width: 90%;

    margin-bottom: 1.5rem;
}

.stat-row {
    display: flex;

    gap: 2.5rem;

    margin-top: 1.5rem;
}

.stat-num {
    font-size: 1.6rem;

    font-weight: 800;
}

.stat-num.green {
    color: #22d3ee;
}

.stat-num.blue {
    color: #60a5fa;
}

.stat-num.purple {
    color: #38bdf8;
}

.stat-label {
    color: #93a3b8;

    font-size: 0.85rem;
}

.why-title,
.hiw-title {
    text-align: center;

    font-size: 2.2rem;

    font-weight: 800;

    color: #f3f4f6;

    margin-top: 1.5rem;
}

.why-sub,
.hiw-sub {
    text-align: center;

    color: #93a3b8;

    max-width: 750px;

    margin:
        0 auto 2.5rem auto;

    line-height: 1.6;
}

.feature-card {
    background: #0d1b2a;

    border:
        1px solid
        #1e3a56;

    border-radius: 14px;

    padding: 1.5rem;

    height: 100%;

    min-height: 220px;

    transition: all 0.2s ease;
}

.feature-card:hover {
    transform:
        translateY(-3px);

    box-shadow:
        0 8px 20px
        rgba(0, 0, 0, 0.5);

    border-color: #2b5478;
}

.feature-icon {
    width: 52px;
    height: 52px;

    border-radius: 12px;

    display: flex;

    align-items: center;
    justify-content: center;

    font-size: 1.6rem;

    margin-bottom: 1rem;
}

.feature-icon.f1 {
    background:
        rgba(96, 165, 250, 0.15);
}

.feature-icon.f2 {
    background:
        rgba(34, 211, 238, 0.15);
}

.feature-icon.f3 {
    background:
        rgba(59, 130, 246, 0.15);
}

.feature-icon.f4 {
    background:
        rgba(56, 189, 248, 0.15);
}

.feature-icon.f5 {
    background:
        rgba(103, 232, 249, 0.15);
}

.feature-icon.f6 {
    background:
        rgba(14, 165, 233, 0.15);
}

.feature-title {
    font-size: 1.15rem;

    font-weight: 800;

    color: #f3f4f6;

    margin-bottom: 0.5rem;
}

.feature-desc {
    color: #93a3b8;

    font-size: 0.92rem;

    line-height: 1.55;
}

.step-badge {
    display: inline-block;

    padding:
        0.3rem 0.9rem;

    border-radius: 999px;

    font-size: 0.8rem;

    font-weight: 700;

    margin-bottom: 0.8rem;
}

.step-badge.b1 {
    background:
        rgba(96, 165, 250, 0.15);

    color: #60a5fa;
}

.step-badge.b2 {
    background:
        rgba(34, 211, 238, 0.15);

    color: #22d3ee;
}

.step-badge.b3 {
    background:
        rgba(59, 130, 246, 0.15);

    color: #93c5fd;
}

.step-title {
    font-size: 1.6rem;

    font-weight: 800;

    color: #f3f4f6;

    margin-bottom: 0.6rem;
}

.step-desc {
    color: #93a3b8;

    line-height: 1.6;

    margin-bottom: 1rem;
}

.step-check {
    color: #cbd5e1;

    margin-bottom: 0.45rem;
}

.step-image {
    width: 100%;

    max-height: 350px;

    object-fit: cover;

    border-radius: 20px;

    border:
        1px solid
        rgba(34, 211, 238, 0.2);

    box-shadow:
        0 12px 35px
        rgba(0, 0, 0, 0.35);
}

.ai-orbit-wrap {
    position: relative;

    height: 320px;

    border-radius: 20px;

    background:
        radial-gradient(
            circle at center,
            #123a52 0%,
            #06283d 55%,
            #030b18 100%
        );

    border: 1px solid rgba(34, 211, 238, 0.25);

    box-shadow:
        0 12px 35px rgba(0, 0, 0, 0.35),
        inset 0 0 60px rgba(6, 182, 212, 0.08);

    overflow: hidden;
}

.ai-orbit-scanlines {
    position: absolute;
    inset: 0;

    background:
        repeating-linear-gradient(
            0deg,
            rgba(34, 211, 238, 0.03) 0px,
            rgba(34, 211, 238, 0.03) 1px,
            transparent 1px,
            transparent 3px
        );

    pointer-events: none;
}

.ai-ring {
    position: absolute;

    top: 50%;
    left: 50%;

    border-radius: 50%;

    border: 1px dashed rgba(34, 211, 238, 0.22);

    transform: translate(-50%, -50%);
}

.ai-ring.r1 { width: 210px; height: 210px; }
.ai-ring.r2 { width: 290px; height: 290px; border-style: solid; border-color: rgba(59, 130, 246, 0.12); }

.ai-core {
    position: absolute;

    top: 50%;
    left: 50%;

    width: 108px;
    height: 108px;

    margin-top: -54px;
    margin-left: -54px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(34, 211, 238, 0.35),
            rgba(59, 130, 246, 0.12)
        );

    border: 2px solid rgba(34, 211, 238, 0.65);

    display: flex;
    align-items: center;
    justify-content: center;

    font-weight: 800;
    font-size: 1.7rem;
    letter-spacing: 1px;
    color: #e6fbff;

    box-shadow:
        0 0 35px rgba(34, 211, 238, 0.45),
        inset 0 0 20px rgba(34, 211, 238, 0.3);

    animation: ai-pulse 2.6s ease-in-out infinite;

    z-index: 3;
}

@keyframes ai-pulse {
    0%, 100% {
        box-shadow:
            0 0 28px rgba(34, 211, 238, 0.35),
            inset 0 0 14px rgba(34, 211, 238, 0.22);
        transform: scale(1);
    }
    50% {
        box-shadow:
            0 0 55px rgba(34, 211, 238, 0.75),
            inset 0 0 26px rgba(34, 211, 238, 0.42);
        transform: scale(1.04);
    }
}

.orbit-item {
    position: absolute;

    top: 50%;
    left: 50%;

    width: 0;
    height: 0;

    animation-name: orbit-spin;
    animation-timing-function: linear;
    animation-iteration-count: infinite;

    z-index: 2;
}

@keyframes orbit-spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.orbit-icon {
    position: absolute;

    width: 46px;
    height: 46px;

    margin-top: -23px;
    margin-left: -23px;

    border-radius: 50%;

    background: #0d1b2a;

    border: 1px solid rgba(34, 211, 238, 0.4);

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 1.4rem;

    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.45);

    animation-name: counter-spin;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
}

@keyframes counter-spin {
    from { transform: translate(var(--radius), 0) rotate(0deg); }
    to   { transform: translate(var(--radius), 0) rotate(-360deg); }
}

.ai-status-pill {
    position: absolute;

    bottom: 16px;
    left: 50%;

    transform: translateX(-50%);

    background: rgba(13, 27, 42, 0.85);

    border: 1px solid rgba(85, 214, 166, 0.35);

    color: #55d6a6;

    font-size: 0.78rem;
    font-weight: 700;

    padding: 6px 14px;

    border-radius: 999px;

    z-index: 3;

    animation: status-fade 2.6s ease-in-out infinite;
}

@keyframes status-fade {
    0%, 100% { opacity: 0.7; }
    50% { opacity: 1; }
}

.dish-wrap {
    position: relative;

    height: 320px;

    border-radius: 20px;

    background:
        radial-gradient(
            circle at center,
            #123a52 0%,
            #06283d 55%,
            #030b18 100%
        );

    border: 1px solid rgba(34, 211, 238, 0.25);

    box-shadow:
        0 12px 35px rgba(0, 0, 0, 0.35),
        inset 0 0 60px rgba(6, 182, 212, 0.08);

    overflow: hidden;
}

.dish-plate-ring {
    position: absolute;

    top: 50%;
    left: 50%;

    width: 190px;
    height: 190px;

    border-radius: 50%;

    transform: translate(-50%, -50%);

    background:
        conic-gradient(
            from 0deg,
            rgba(34, 211, 238, 0) 0%,
            rgba(34, 211, 238, 0.6) 12%,
            rgba(34, 211, 238, 0) 32%
        );

    filter: blur(1px);

    animation: ring-rotate 5s linear infinite;

    z-index: 1;
}

@keyframes ring-rotate {
    from { transform: translate(-50%, -50%) rotate(0deg); }
    to   { transform: translate(-50%, -50%) rotate(360deg); }
}

.dish-plate {
    position: absolute;

    top: 50%;
    left: 50%;

    width: 168px;
    height: 168px;

    margin-top: -84px;
    margin-left: -84px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            #1c2b3d 0%,
            #0d1b2a 75%
        );

    border: 3px solid rgba(34, 211, 238, 0.4);

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 4.2rem;

    box-shadow:
        0 0 40px rgba(34, 211, 238, 0.35),
        inset 0 4px 18px rgba(0, 0, 0, 0.55);

    animation: dish-float 3.4s ease-in-out infinite;

    z-index: 3;
}

@keyframes dish-float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-7px); }
}

.steam-wisp {
    position: absolute;

    bottom: 56%;

    width: 6px;
    height: 40px;

    border-radius: 50%;

    background:
        linear-gradient(
            to top,
            rgba(255, 255, 255, 0.55),
            rgba(255, 255, 255, 0)
        );

    filter: blur(2px);

    animation-name: steam-rise;
    animation-timing-function: ease-in-out;
    animation-iteration-count: infinite;

    z-index: 4;
}

@keyframes steam-rise {
    0%   { transform: translateY(0) scaleX(1); opacity: 0; }
    15%  { opacity: 0.6; }
    50%  { transform: translateY(-45px) scaleX(1.4); opacity: 0.4; }
    100% { transform: translateY(-90px) scaleX(1.9); opacity: 0; }
}

.dish-badge {
    position: absolute;

    background: rgba(13, 27, 42, 0.85);

    border: 1px solid rgba(34, 211, 238, 0.3);

    border-radius: 12px;

    padding: 8px 12px;

    text-align: center;

    font-size: 0.78rem;
    font-weight: 700;

    color: #e6fbff;

    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35);

    z-index: 3;

    animation: status-fade 3s ease-in-out infinite;
}

.dish-badge .icon {
    font-size: 1.3rem;
    display: block;
    margin-bottom: 4px;
}

.dish-badge.top-left { top: 18px; left: 18px; }
.dish-badge.top-right { top: 18px; right: 18px; }
.dish-badge.bottom-left { bottom: 18px; left: 18px; }
.dish-badge.bottom-right { bottom: 18px; right: 18px; }

.snap-wrap {
    position: relative;

    height: 320px;

    border-radius: 20px;

    background:
        radial-gradient(
            circle at center,
            #123a52 0%,
            #06283d 55%,
            #030b18 100%
        );

    border: 1px solid rgba(34, 211, 238, 0.25);

    box-shadow:
        0 12px 35px rgba(0, 0, 0, 0.35),
        inset 0 0 60px rgba(6, 182, 212, 0.08);

    overflow: hidden;
}

.snap-scanline {
    position: absolute;

    left: 8%;
    right: 8%;

    height: 3px;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(34, 211, 238, 0.9),
            transparent
        );

    box-shadow: 0 0 14px rgba(34, 211, 238, 0.8);

    animation: snap-scan 3.4s ease-in-out infinite;

    z-index: 2;
}

@keyframes snap-scan {
    0%   { top: 14%; opacity: 0; }
    10%  { opacity: 1; }
    50%  { top: 86%; opacity: 1; }
    62%  { opacity: 0; }
    100% { top: 14%; opacity: 0; }
}

.snap-camera {
    position: absolute;

    top: 50%;
    left: 50%;

    width: 100px;
    height: 100px;

    margin-top: -50px;
    margin-left: -50px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(34, 211, 238, 0.32),
            rgba(59, 130, 246, 0.12)
        );

    border: 2px solid rgba(34, 211, 238, 0.62);

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 2.7rem;

    box-shadow:
        0 0 32px rgba(34, 211, 238, 0.4),
        inset 0 0 18px rgba(34, 211, 238, 0.25);

    animation: ai-pulse 2.4s ease-in-out infinite;

    z-index: 3;
}

.snap-flash {
    position: absolute;

    top: 50%;
    left: 50%;

    width: 100px;
    height: 100px;

    margin-top: -50px;
    margin-left: -50px;

    border-radius: 50%;

    border: 2px solid rgba(255, 255, 255, 0.65);

    animation: snap-flash 3.4s ease-out infinite;

    z-index: 2;
}

@keyframes snap-flash {
    0%, 45% { transform: scale(1); opacity: 0; }
    50%     { opacity: 0.85; }
    72%     { transform: scale(2.5); opacity: 0; }
    100%    { opacity: 0; }
}

.snap-item {
    position: absolute;

    width: 50px;
    height: 50px;

    border-radius: 50%;

    background: #0d1b2a;

    border: 1px solid rgba(34, 211, 238, 0.4);

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 1.5rem;

    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.45);

    animation-name: snap-item-fade;
    animation-timing-function: ease-in-out;
    animation-iteration-count: infinite;

    z-index: 2;
}

@keyframes snap-item-fade {
    0%, 100% { opacity: 0.28; transform: scale(0.85); }
    50%      { opacity: 1; transform: scale(1); }
}

.snap-item.top-left { top: 16%; left: 16%; }
.snap-item.top-right { top: 16%; right: 16%; }
.snap-item.bottom-left { bottom: 16%; left: 16%; }
.snap-item.bottom-right { bottom: 16%; right: 16%; }

.footer-wrap {
    margin-top: 70px;

    background: #0b1528;

    color: #dbe7f5;

    border-top:
        1px solid
        rgba(255, 255, 255, 0.08);

    border-radius:
        20px 20px 0 0;

    overflow: hidden;
}

.footer-top {
    display: grid;

    grid-template-columns:
        1.5fr 1fr 1fr 1.2fr;

    gap: 45px;

    padding:
        50px 35px 45px;
}

.footer-brand-title {
    font-size: 27px;

    font-weight: 800;

    color: #ffffff;

    margin-bottom: 8px;
}

.footer-brand-tagline {
    font-size: 15px;

    font-weight: 600;

    color: #55d6a6;

    margin-bottom: 15px;
}

.footer-brand-desc {
    max-width: 390px;

    color: #94a8c2;

    font-size: 14px;

    line-height: 1.8;
}

.footer-social {
    display: flex;

    gap: 10px;

    margin-top: 22px;
}

.footer-social a {
    width: 40px;
    height: 40px;

    display: flex;

    align-items: center;
    justify-content: center;

    background: #16243a;

    border:
        1px solid
        rgba(255, 255, 255, 0.07);

    border-radius: 10px;

    text-decoration: none;

    font-size: 18px;

    transition: all 0.25s ease;
}

.footer-social a:hover {
    transform:
        translateY(-3px);

    background: #1c314b;
}

.footer-col-title {
    color: #ffffff;

    font-size: 17px;

    font-weight: 750;

    margin-bottom: 20px;
}

.footer-col a {
    display: block;

    color: #94a8c2;

    text-decoration: none;

    font-size: 14px;

    margin-bottom: 13px;

    transition: all 0.2s ease;
}

.footer-col a:hover {
    color: #55d6a6;

    transform:
        translateX(3px);
}

.footer-mission p {
    margin: 0;

    color: #94a8c2;

    font-size: 14px;

    line-height: 1.7;
}

.footer-highlight {
    display: inline-block;

    margin-top: 18px;

    padding: 12px 16px;

    background: #12233a;

    border:
        1px solid
        rgba(85, 214, 166, 0.15);

    border-radius: 10px;
}

.footer-highlight strong {
    color: #ffffff;

    font-size: 14px;
}

.footer-highlight span {
    color: #55d6a6;

    font-size: 13px;
}

.footer-divider {
    height: 1px;

    background:
        rgba(255, 255, 255, 0.08);

    margin: 0 35px;
}

.footer-stats {
    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    text-align: center;

    padding:
        28px 35px;
}

.footer-stat-num {
    font-size: 23px;

    font-weight: 800;

    color: #55d6a6;
}

.footer-stat-label {
    margin-top: 5px;

    color: #8095ae;

    font-size: 12px;
}

.footer-bottom {
    border-top:
        1px solid
        rgba(255, 255, 255, 0.07);

    padding:
        20px 35px;

    display: flex;

    justify-content: space-between;

    align-items: center;

    color: #71859d;

    font-size: 12px;
}

.footer-bottom-links {
    display: flex;

    gap: 22px;
}

.footer-bottom a {
    color: #71859d;

    text-decoration: none;
}

.footer-bottom a:hover {
    color: #55d6a6;
}

@media (max-width: 900px) {

    .footer-top {
        grid-template-columns:
            1fr 1fr;

        gap: 35px;
    }

    .footer-stats {
        grid-template-columns:
            repeat(2, 1fr);

        gap: 20px;
    }

    .footer-bottom {
        flex-direction: column;

        gap: 15px;

        text-align: center;
    }

    .hero-title {
        font-size: 2.4rem;
    }
}

@media (max-width: 600px) {

    .navbar {
        margin-top: -1rem;
        margin-bottom: 3rem;

        padding:
            0.8rem 1rem;
    }

    .hero-title {
        font-size: 2rem;
    }

    .stat-row {
        gap: 1.2rem;

        flex-wrap: wrap;
    }

    .footer-top {
        grid-template-columns: 1fr;

        padding:
            40px 25px;
    }

    .footer-stats {
        grid-template-columns:
            1fr 1fr;

        padding:
            25px 20px;
    }

    .footer-bottom {
        padding: 20px;
    }
}

</style>
""",
    unsafe_allow_html=True
)

LANGUAGES = {
    "English": "en",
    "हिंदी": "hi",
    "বাংলা": "bn",
    "தமிழ்": "ta",
    "తెలుగు": "te",
    "मराठी": "mr",
    "ગુજરાતી": "gu",
    "ಕನ್ನಡ": "kn",
    "മലയാളം": "ml",
    "ਪੰਜਾਬੀ": "pa",
    "اردو": "ur"
}

if "language_code" not in st.session_state:
    st.session_state.language_code = "en"

if "language_name" not in st.session_state:
    st.session_state.language_name = "English"

def load_translation(language_code):

    translation_path = os.path.join(
        TRANSLATION_DIR,
        f"{language_code}.json"
    )

    fallback_path = os.path.join(
        TRANSLATION_DIR,
        "en.json"
    )

    try:
        with open(
            translation_path,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):

        try:
            with open(
                fallback_path,
                "r",
                encoding="utf-8"
            ) as file:
                return json.load(file)

        except Exception:
            return {}

T = load_translation(
    st.session_state.language_code
)

if "camera_images" not in st.session_state:
    st.session_state.camera_images = []

if "camera_active" not in st.session_state:
    st.session_state.camera_active = False

if "fridge_audio" not in st.session_state:
    st.session_state.fridge_audio = None

if "fridge_audio_widget_version" not in st.session_state:
    st.session_state.fridge_audio_widget_version = 0

def get_text(key, default):
    """Look up `key` in the active translation dict, falling back
    to `default` (English) if the key is missing."""
    return T.get(key, default)

def get_base64_image(path):

    try:

        with open(path, "rb") as f:
            return base64.b64encode(
                f.read()
            ).decode()

    except (FileNotFoundError, OSError):
        return None

navbar_logo_path = os.path.join(
    IMAGE_DIR,
    "foodrescue_icon_256.png"
)

navbar_logo_b64 = get_base64_image(
    navbar_logo_path
)

navbar_title_text = get_text("navbar_title", "FoodRescue AI")
navbar_tagline_text = get_text(
    "navbar_tagline", "Smart Fridge-to-Recipe Detection"
)

if navbar_logo_b64:

    st.markdown(
        f"""<div class="navbar"><img src="data:image/png;base64,{navbar_logo_b64}" class="navbar-logo" /><div><div class="navbar-title">{navbar_title_text}</div><div class="navbar-tagline">{navbar_tagline_text}</div></div></div>""",
        unsafe_allow_html=True
    )

else:

    st.markdown(
        f"""<div class="navbar"><div style="font-size:1.8rem;width:44px;text-align:center;">🍃</div><div><div class="navbar-title">{navbar_title_text}</div><div class="navbar-tagline">{navbar_tagline_text}</div></div></div>""",
        unsafe_allow_html=True
    )

language_col1, language_col2 = st.columns(
    [5, 1]
)

with language_col2:

    selected_language = st.selectbox(
        get_text("language_label", "🌐 Language"),
        list(LANGUAGES.keys()),
        index=list(LANGUAGES.values()).index(
            st.session_state.language_code
        ),
        key="language_selector"
    )

    new_language_code = LANGUAGES[
        selected_language
    ]

    if (
        new_language_code
        != st.session_state.language_code
    ):

        st.session_state.language_code = (
            new_language_code
        )

        st.session_state.language_name = (
            selected_language
        )

        st.rerun()

T = load_translation(
    st.session_state.language_code
)

hero_left, hero_right = st.columns(
    [1.1, 1]
)

with hero_left:

    badge_pill_text = get_text(
        "badge_pill", "🍳 AI-Powered Ingredient Detection"
    )
    hero_title_line1 = get_text(
        "hero_title_line1", "Turn Your Fridge"
    )
    hero_title_highlight = get_text(
        "hero_title_highlight", "Feast"
    )
    hero_title_suffix = get_text(
        "hero_title_suffix", "with AI"

    )
    hero_title_connector = get_text("hero_title_connector", "into a ")
    hero_sub_text = get_text(
        "hero_sub",
        "Snap a photo of whatever's left in your fridge — "
        "our AI identifies the ingredients and instantly "
        "generates a custom recipe, so nothing goes to waste."
    )
    stat_free_num = get_text("stat_free_num", "100%")
    stat_free_label = get_text("stat_free_label", "Free to Use")
    stat_time_num = get_text("stat_time_num", "5 sec")
    stat_time_label = get_text("stat_time_label", "Avg. Detection Time")
    stat_recipe_num = get_text("stat_recipe_num", "∞")
    stat_recipe_label = get_text("stat_recipe_label", "Recipe Ideas")

    st.markdown(
        f"""<div class="badge-pill">{badge_pill_text}</div><div class="hero-title">{hero_title_line1}<br>{hero_title_connector}<span class="highlight">{hero_title_highlight}</span> {hero_title_suffix}</div><div class="hero-sub">{hero_sub_text}</div><div class="stat-row"><div><div class="stat-num green">{stat_free_num}</div><div class="stat-label">{stat_free_label}</div></div><div><div class="stat-num blue">{stat_time_num}</div><div class="stat-label">{stat_time_label}</div></div><div><div class="stat-num purple">{stat_recipe_num}</div><div class="stat-label">{stat_recipe_label}</div></div></div>""",
        unsafe_allow_html=True
    )

images_to_process = []

with hero_right:

    with st.container(border=True):

        st.markdown(
            f"#### {get_text('get_started_header', '📸 Get Started')}"
        )

        st.caption(
            get_text(
                "get_started_caption",
                "Choose how you'd like to add a photo "
                "of your fridge"
            )
        )

        take_photo_text = get_text(
            "take_photo",
            "📷 Take a photo"
        )

        upload_text = get_text(
            "upload_files",
            "📁 Upload files"
        )

        voice_text = get_text(
            "voice",
            "🎤 Describe by voice"
        )

        input_method = st.radio(
            get_text(
                "choose_photo",
                "Choose input method"
            ),
            [
                take_photo_text,
                upload_text,
                voice_text
            ],
            label_visibility="collapsed",
            key="input_method"
        )

        if input_method == take_photo_text:

            with st.container(border=True):

                st.write(
                    get_text(
                        "camera_access",
                        "Camera access ({current}/{max} photos taken)"
                    ).format(
                        current=len(st.session_state.camera_images),
                        max=MAX_IMAGES
                    )
                )

                camera_on = st.toggle(
                    get_text("turn_on_camera", "Turn on camera"),
                    value=st.session_state.camera_active,
                    key="camera_toggle_widget"
                )

                st.session_state.camera_active = (
                    camera_on
                )

                if camera_on:

                    if (
                        len(
                            st.session_state.camera_images
                        )
                        < MAX_IMAGES
                    ):

                        camera_photo = st.camera_input(
                            get_text("take_a_photo_label", "Take a photo"),
                            label_visibility="collapsed",
                            key="camera_input_widget"
                        )

                        if camera_photo is not None:

                            existing_names = [
                                getattr(
                                    img,
                                    "name",
                                    ""
                                )
                                for img in
                                st.session_state.camera_images
                            ]

                            current_name = getattr(
                                camera_photo,
                                "name",
                                ""
                            )

                            if current_name not in existing_names:

                                st.session_state.camera_images.append(
                                    camera_photo
                                )

                                st.rerun()

                    else:

                        st.info(
                            get_text(
                                "max_photos_reached",
                                "✅ You've reached the maximum "
                                "of {max} photos."
                            ).format(max=MAX_IMAGES)
                        )

                else:

                    st.caption(
                        get_text(
                            "camera_off_caption",
                            "Camera is off. "
                            "Turn it on to take a photo."
                        )
                    )

            if st.session_state.camera_images:

                st.write(
                    f"**{get_text('photos_clicked', '{n} photo(s) clicked').format(n=len(st.session_state.camera_images))}**"
                )

                cols = st.columns(
                    len(
                        st.session_state.camera_images
                    )
                )

                for idx, img in enumerate(
                    st.session_state.camera_images
                ):

                    with cols[idx]:

                        st.image(
                            img,
                            caption=get_text(
                                "photo_caption", "Photo {n}"
                            ).format(n=idx + 1),
                            width=120
                        )

                        if st.button(
                            get_text("remove_photo", "❌ Remove"),
                            key=f"remove_camera_{idx}"
                        ):

                            st.session_state.camera_images.pop(
                                idx
                            )

                            st.rerun()

                if st.button(
                    get_text("clear_all_photos", "🗑️ Clear All Photos"),
                    key="clear_camera_photos"
                ):

                    st.session_state.camera_images = []

                    st.rerun()

            images_to_process = (
                st.session_state.camera_images
            )

        elif input_method == upload_text:

            with st.form("upload_form"):

                uploaded_images = st.file_uploader(
                    get_text(
                        "upload_label",
                        "Upload photos of your fridge "
                        "(max 5)"
                    ),
                    type=[
                        "jpg",
                        "jpeg",
                        "png"
                    ],
                    accept_multiple_files=True
                )

                submitted = st.form_submit_button(
                    get_text("confirm_photos", "✅ Confirm Photos")
                )

                if submitted:

                    if not uploaded_images:

                        st.warning(
                            get_text(
                                "upload_warning_empty",
                                "Please select at least "
                                "one image."
                            )
                        )

                    else:

                        if len(uploaded_images) > MAX_IMAGES:

                            st.warning(
                                get_text(
                                    "upload_warning_max",
                                    "⚠️ Only {max} images are "
                                    "allowed. The first {max} "
                                    "will be used."
                                ).format(max=MAX_IMAGES)
                            )

                            uploaded_images = (
                                uploaded_images[
                                    :MAX_IMAGES
                                ]
                            )

                        st.session_state.confirmed_uploads = (
                            uploaded_images
                        )

            if "confirmed_uploads" in st.session_state:

                images_to_process = (
                    st.session_state.confirmed_uploads
                )

                st.write(
                    f"**{get_text('photos_confirmed', '{n} photo(s) confirmed').format(n=len(images_to_process))}**"
                )

                cols = st.columns(
                    len(images_to_process)
                )

                for idx, img in enumerate(
                    images_to_process
                ):

                    with cols[idx]:

                        st.image(
                            img,
                            caption=get_text(
                                "photo_caption", "Photo {n}"
                            ).format(n=idx + 1),
                            width=120
                        )

        else:

            with st.container(border=True):

                st.caption(
                    get_text(
                        "voice_caption",
                        'Just say out loud what\'s in your '
                        'fridge — e.g. "I have eggs, half a '
                        'block of cheese, some spinach, and '
                        'leftover rice." We\'ll transcribe it '
                        'and pull out the ingredients.'
                    )
                )

                audio_value = st.audio_input(
                    get_text(
                        "record_voice_label",
                        "Record a voice note describing "
                        "your fridge contents"
                    ),
                    key=(
                        "fridge_audio_widget_"
                        f"{st.session_state.fridge_audio_widget_version}"
                    )
                )

                if audio_value is not None:

                    st.session_state.fridge_audio = (
                        audio_value
                    )

                if (
                    st.session_state.fridge_audio
                    is not None
                ):

                    st.audio(
                        st.session_state.fridge_audio
                    )

                    if st.button(
                        get_text("clear_recording", "🗑️ Clear Recording"),
                        key="clear_recording"
                    ):

                        st.session_state.fridge_audio = (
                            None
                        )

                        st.session_state.fridge_audio_widget_version += 1

                        st.rerun()

        has_images = bool(
            images_to_process
        )

        has_audio = (
            input_method == voice_text
            and
            st.session_state.fridge_audio
            is not None
        )

        if has_images or has_audio:

            st.markdown("")

            if st.button(
                get_text(
                    "analyze",
                    "🔍 Analyze Ingredients"
                ),
                key="analyze_button"
            ):

                with st.spinner(
                    get_text(
                        "analyzing_spinner",
                        "Identifying ingredients..."
                    )
                ):

                    try:

                        if has_images:

                            files_payload = []

                            for i, img in enumerate(
                                images_to_process
                            ):

                                mime_type = getattr(
                                    img,
                                    "type",
                                    None
                                ) or "image/jpeg"

                                files_payload.append(
                                    (
                                        "images",
                                        (
                                            f"photo_{i}.jpg",
                                            img.getvalue(),
                                            mime_type
                                        )
                                    )
                                )

                            response = requests.post(
                                f"{BACKEND_URL}/analyze-fridge",
                                files=files_payload,
                                data={
                                    "language":
                                        st.session_state.language_code
                                },
                                timeout=120
                            )

                        else:

                            audio_bytes = (
                                st.session_state
                                .fridge_audio
                                .getvalue()
                            )

                            audio_mime = getattr(
                                st.session_state
                                .fridge_audio,
                                "type",
                                "audio/wav"
                            ) or "audio/wav"

                            files_payload = [
                                (
                                    "audio",
                                    (
                                        "fridge_audio.wav",
                                        audio_bytes,
                                        audio_mime
                                    )
                                )
                            ]

                            response = requests.post(
                                f"{BACKEND_URL}/analyze-fridge-audio",
                                files=files_payload,
                                data={
                                    "language":
                                        st.session_state.language_code
                                },
                                timeout=120
                            )

                        if response.status_code == 200:

                            data = response.json()

                            ingredients = data.get(
                                "ingredients",
                                []
                            )

                            st.session_state.detected_ingredients = (
                                sorted(
                                    set(
                                        ingredients
                                    )
                                )
                            )

                            st.session_state.pop(
                                "recipes",
                                None
                            )

                            st.session_state.pop(
                                "recipe",
                                None
                            )

                            st.session_state.pop(
                                "recipe_image",
                                None
                            )

                            st.session_state.pop(
                                "ingredients_df",
                                None
                            )

                            st.success(
                                get_text(
                                    "ingredients_detected_success",
                                    "Ingredients detected successfully!"
                                )
                            )

                        else:

                            try:

                                err = response.json().get(
                                    "error",
                                    response.text
                                )

                            except Exception:

                                err = response.text

                            st.error(
                                get_text(
                                    "detect_error_prefix",
                                    "Could not detect ingredients: {err}"
                                ).format(err=err)
                            )

                    except requests.exceptions.ConnectionError:

                        st.error(
                            get_text(
                                "backend_unreachable",
                                "⚠️ Backend not reachable. "
                                "Please start your backend server."
                            )
                        )

                    except requests.exceptions.Timeout:

                        st.error(
                            get_text(
                                "request_timeout",
                                "⏱️ Request timed out. "
                                "Please try again."
                            )
                        )

                    except Exception as e:

                        st.error(
                            get_text(
                                "unexpected_error_prefix",
                                "Unexpected error: {err}"
                            ).format(err=str(e))
                        )

if "detected_ingredients" in st.session_state:

    with st.container(border=True):

        col1, col2 = st.columns(
            [1, 2]
        )

        with col1:

            st.metric(
                f"🥕 {get_text(
                    'ingredients_found',
                    'Ingredients Found'
                )}",
                len(
                    st.session_state
                    .detected_ingredients
                )
            )

        with col2:

            st.write(
                f"**{get_text(
                    'edit_ingredients',
                    'Edit Ingredients'
                )}** "
                f"{get_text(
                    'edit_ingredients_hint',
                    '(add quantity, remove wrong '
                    'items, add new ones):'
                )}"
            )

            if "ingredients_df" not in st.session_state:

                st.session_state.ingredients_df = (
                    pd.DataFrame(
                        {
                            "Ingredient":
                                st.session_state
                                .detected_ingredients,

                            "Quantity":
                                [
                                    ""
                                    for _
                                    in st.session_state
                                    .detected_ingredients
                                ],

                            "Include in Recipe":
                                [
                                    True
                                    for _
                                    in st.session_state
                                    .detected_ingredients
                                ]
                        }
                    )
                )

            edited_df = st.data_editor(
                st.session_state.ingredients_df,

                num_rows="dynamic",

                use_container_width=True,

                column_config={

                    "Ingredient":
                        st.column_config.TextColumn(
                            get_text("col_ingredient", "Ingredient"),
                            required=True
                        ),

                    "Quantity":
                        st.column_config.TextColumn(
                            get_text("col_quantity", "Quantity (optional)")
                        ),

                    "Include in Recipe":
                        st.column_config.CheckboxColumn(
                            get_text("col_use", "Use?"),
                            default=True
                        )
                },

                key="ingredients_editor"
            )

            st.session_state.ingredients_df = (
                edited_df
            )

    st.markdown("")

    serving = st.number_input(
        get_text(
            "serving",
            "Servings"
        ),

        min_value=1,

        max_value=10,

        value=st.session_state.get(
            "servings_value",
            2
        ),

        step=1,

        key="servings_value"
    )

    if st.button(
        get_text(
            "generate_recipe",
            "🍽️ Generate Recipes"
        ),
        key="generate_recipe_button"
    ):

        active_ingredients = (
            st.session_state.ingredients_df[
                st.session_state.ingredients_df[
                    "Include in Recipe"
                ] == True
            ]["Ingredient"]
            .dropna()
            .astype(str)
            .str.strip()
            .tolist()
        )

        active_ingredients = [
            x
            for x in active_ingredients
            if x
        ]

        if not active_ingredients:

            st.warning(
                get_text(
                    "select_ingredient_warning",
                    "⚠️ Select at least one "
                    "ingredient to generate a recipe."
                )
            )

        else:

            with st.spinner(
                get_text(
                    "generating_recipes_spinner",
                    "Generating 2 recipe options..."
                )
            ):

                try:

                    recipe_response = requests.post(
                        f"{BACKEND_URL}/generate-recipe",

                        json={
                            "ingredients":
                                active_ingredients,

                            "servings":
                                serving,

                            "language":
                                st.session_state.language_code
                        },

                        timeout=180
                    )

                    if recipe_response.status_code == 200:

                        try:

                            result = (
                                recipe_response.json()
                            )

                        except ValueError:

                            st.error(
                                get_text(
                                    "recipe_gen_failed_invalid",
                                    "Recipe generation failed: "
                                    "invalid response from server."
                                )
                            )

                            result = None

                        if result is not None:

                            if "error" in result:

                                st.error(
                                    get_text(
                                        "recipe_gen_error_prefix",
                                        "Error: {err}"
                                    ).format(err=result['error'])
                                )

                            else:

                                st.session_state.recipes = (
                                    result.get(
                                        "recipes",
                                        []
                                    )
                                )

                                st.session_state.pop(
                                    "recipe",
                                    None
                                )

                                st.session_state.pop(
                                    "recipe_image",
                                    None
                                )

                    else:

                        st.error(
                            get_text(
                                "recipe_gen_failed_prefix",
                                "Recipe generation failed: {err}"
                            ).format(err=recipe_response.text)
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        get_text(
                            "backend_unreachable",
                            "⚠️ Backend not reachable."
                        )
                    )

                except requests.exceptions.Timeout:

                    st.error(
                        get_text(
                            "recipe_gen_timeout",
                            "⏱️ Recipe generation timed out."
                        )
                    )

                except Exception as e:

                    st.error(
                        get_text(
                            "unexpected_error_prefix",
                            "Unexpected error: {err}"
                        ).format(err=str(e))
                    )

    if (
        "recipes" in st.session_state
        and
        "recipe" not in st.session_state
    ):

        st.write(
            get_text(
                "choose_two_options",
                "### 🍽️ Choose one of the two options:"
            )
        )

        recipes = st.session_state.recipes

        if not recipes:

            st.warning(
                get_text(
                    "no_recipes_warning",
                    "No recipes were returned."
                )
            )

        else:

            option_cols = st.columns(
                len(recipes)
            )

            for idx, opt in enumerate(
                recipes
            ):

                with option_cols[idx]:

                    with st.container(
                        border=True
                    ):

                        st.subheader(
                            get_text(
                                "option_prefix",
                                "Option {n}: {name}"
                            ).format(
                                n=idx + 1,
                                name=opt.get(
                                    'recipe_name',
                                    get_text(
                                        "recipe_fallback_name",
                                        "Recipe"
                                    )
                                )
                            )
                        )

                        oc1, oc2 = st.columns(2)

                        oc1.metric(
                            get_text("prep_time", "⏱️ Prep Time"),
                            opt.get(
                                "prep_time",
                                "-"
                            )
                        )

                        oc2.metric(
                            get_text("servings_label", "🍽️ Servings"),
                            opt.get(
                                "servings",
                                "-"
                            )
                        )

                        st.write(
                            get_text(
                                "steps_preview",
                                "**Steps preview:**"
                            )
                        )

                        steps = opt.get(
                            "steps",
                            []
                        )

                        for i, step in enumerate(
                            steps[:3],
                            1
                        ):

                            st.write(
                                f"{i}. {step}"
                            )

                        if len(steps) > 3:

                            st.caption(
                                get_text(
                                    "more_steps_suffix",
                                    "...+{n} more steps"
                                ).format(n=len(steps) - 3)
                            )

                        if st.button(
                            get_text(
                                "make_this_recipe",
                                "✅ Make This Recipe"
                            ),
                            key=f"choose_recipe_{idx}"
                        ):

                            st.session_state.recipe = (
                                opt
                            )

                            st.session_state.pop(
                                "recipe_image",
                                None
                            )

                            st.rerun()

    if "recipe" in st.session_state:

        recipe = st.session_state.recipe

        with st.container(
            border=True
        ):

            top_col, back_col = st.columns(
                [4, 1]
            )

            with top_col:

                st.subheader(
                    get_text(
                        "recipe_title_prefix",
                        "🍽️ {name}"
                    ).format(
                        name=recipe.get(
                            'recipe_name',
                            get_text(
                                "recipe_fallback_name",
                                "Recipe"
                            )
                        )
                    )
                )

            with back_col:

                if st.button(
                    get_text("other_option", "↩️ Other option"),
                    key="other_recipe_option"
                ):

                    st.session_state.pop(
                        "recipe",
                        None
                    )

                    st.session_state.pop(
                        "recipe_image",
                        None
                    )

                    st.rerun()

            c1, c2, c3 = st.columns(3)

            c1.metric(
                get_text("prep_time", "⏱️ Prep Time"),
                recipe.get(
                    "prep_time",
                    "-"
                )
            )

            c2.metric(
                get_text("servings_label", "🍽️ Servings"),
                recipe.get(
                    "servings",
                    serving
                )
            )

            active_count = len(
                st.session_state.ingredients_df[
                    st.session_state.ingredients_df[
                        "Include in Recipe"
                    ] == True
                ]
            )

            c3.metric(
                get_text("ingredients_used", "🥗 Ingredients Used"),
                active_count
            )

            if "recipe_image" not in st.session_state:

                with st.spinner(
                    get_text(
                        "generating_image_spinner",
                        "🎨 Generating recipe image..."
                    )
                ):

                    try:

                        img_response = requests.post(
                            f"{BACKEND_URL}/generate-recipe-image",

                            json={
                                "recipe_name":
                                    recipe.get(
                                        "recipe_name",
                                        "Food"
                                    )
                            },

                            timeout=180
                        )

                        if (
                            img_response.status_code
                            == 200
                        ):

                            image_data = (
                                img_response
                                .json()
                                .get("image")
                            )

                            st.session_state.recipe_image = (
                                image_data
                            )

                        else:

                            st.session_state.recipe_image = (
                                None
                            )

                            st.error(
                                get_text(
                                    "image_gen_failed_prefix",
                                    "Image generation failed: {err}"
                                ).format(err=img_response.text)
                            )

                    except requests.exceptions.ConnectionError:

                        st.session_state.recipe_image = (
                            None
                        )

                        st.error(
                            get_text(
                                "backend_unreachable",
                                "⚠️ Backend not reachable."
                            )
                        )

                    except requests.exceptions.Timeout:

                        st.session_state.recipe_image = (
                            None
                        )

                        st.error(
                            get_text(
                                "recipe_gen_timeout",
                                "⏱️ Image generation timed out."
                            )
                        )

                    except Exception as e:

                        st.session_state.recipe_image = (
                            None
                        )

                        st.error(
                            get_text(
                                "image_error_prefix",
                                "Image error: {err}"
                            ).format(err=str(e))
                        )

            if st.session_state.get(
                "recipe_image"
            ):

                try:

                    img_col_left, img_col_center, img_col_right = st.columns(
                        [1, 2, 1]
                    )

                    with img_col_center:

                        st.markdown(
                            f"""<div style="width:100%;max-width:520px;height:400px;margin:0 auto;border-radius:20px;overflow:hidden;border:1px solid rgba(34,211,238,0.25);box-shadow:0 12px 35px rgba(0,0,0,0.35);"><img src="data:image/png;base64,{st.session_state.recipe_image}" style="width:100%;height:100%;object-fit:cover;display:block;" /></div>""",
                            unsafe_allow_html=True
                        )

                        st.caption(
                            recipe.get(
                                "recipe_name",
                                get_text("recipe_fallback_name", "Recipe")
                            )
                        )

                except Exception:

                    st.warning(
                        get_text(
                            "recipe_image_display_error",
                            "Recipe image could not be displayed."
                        )
                    )
            st.write(
                get_text("steps_header", "### 📝 Steps:")
            )

            for i, step in enumerate(
                recipe.get(
                    "steps",
                    []
                ),
                1
            ):

                st.write(
                    f"{i}. {step}"
                )

st.divider()

why_title_text = get_text("why_title", "Why Choose FoodRescue AI?")
why_sub_text = get_text(
    "why_sub",
    "Smart vision meets generative AI to transform the "
    "ingredients you already have into practical, "
    "personalized meals — helping you cook smarter and "
    "waste less."
)

st.markdown(
    f"""<div class="why-title">{why_title_text}</div><div class="why-sub">{why_sub_text}</div>""",
    unsafe_allow_html=True
)

why_features = [

    (
        "f1",
        "🧠",
        get_text("feature1_title", "Smart Ingredient Recognition"),
        get_text(
            "feature1_desc",
            "AI analyzes your fridge photos and identifies "
            "visible ingredients with intelligent image understanding."
        )
    ),

    (
        "f2",
        "🌐",
        get_text("feature2_title", "Multi-Photo & Voice Intelligence"),
        get_text(
            "feature2_desc",
            "Capture up to 5 photos, or simply speak what's "
            "in your fridge — we'll transcribe your voice note "
            "and combine everything into one complete ingredient list."
        )
    ),

    (
        "f3",
        "🤖",
        get_text("feature3_title", "Powered by Gemini Vision"),
        get_text(
            "feature3_desc",
            "Leverage Gemini's advanced vision capabilities "
            "to understand food images and identify ingredients."
        )
    ),

    (
        "f4",
        "🍽️",
        get_text("feature4_title", "Personalized Recipe Creation"),
        get_text(
            "feature4_desc",
            "Turn the ingredients you already have into a "
            "practical recipe with servings, prep time, and clear instructions."
        )
    ),

    (
        "f5",
        "✅",
        get_text("feature5_title", "You Stay in Control"),
        get_text(
            "feature5_desc",
            "Review your detected ingredients, correct mistakes, "
            "add missing items, or remove anything you don't want to use."
        )
    ),

    (
        "f6",
        "🎨",
        get_text("feature6_title", "Visualize Your Dish"),
        get_text(
            "feature6_desc",
            "Get an AI-generated preview of your finished meal "
            "and see the delicious result before you start cooking."
        )
    )
]

feature_cols_1 = st.columns(4)

for i in range(4):

    icon_class, emoji, title, desc = (
        why_features[i]
    )

    with feature_cols_1[i]:

        st.markdown(
            f"""<div class="feature-card"><div class="feature-icon {icon_class}">{emoji}</div><div class="feature-title">{title}</div><div class="feature-desc">{desc}</div></div>""",
            unsafe_allow_html=True
        )

st.markdown(
    "<br>",
    unsafe_allow_html=True
)

feature_cols_2 = st.columns(
    [1, 1, 1, 1]
)

for i in range(4, 6):

    icon_class, emoji, title, desc = (
        why_features[i]
    )

    with feature_cols_2[i - 4]:

        st.markdown(
            f"""<div class="feature-card"><div class="feature-icon {icon_class}">{emoji}</div><div class="feature-title">{title}</div><div class="feature-desc">{desc}</div></div>""",
            unsafe_allow_html=True
        )

st.divider()

hiw_title_text = get_text("hiw_title", "How It Works")
hiw_sub_text = get_text(
    "hiw_sub", "Rescue your leftovers in three simple steps"
)

st.markdown(
    f"""<div class="hiw-title">{hiw_title_text}</div><div class="hiw-sub">{hiw_sub_text}</div>""",
    unsafe_allow_html=True
)

s1_text, s1_image = st.columns(
    [1.3, 1]
)

with s1_text:

    st.markdown(
        f"""<div class="step-badge b1">{get_text("step1_badge", "Step 1")}</div><div class="step-title">{get_text("step1_title", "Snap Your Fridge")}</div><div class="step-desc">{get_text("step1_desc", "Start by showing us what's inside your fridge. Take a live photo, upload up to 5 images, or simply speak out loud what you have — our AI is designed to work across different angles, lighting conditions, and even plain voice notes.")}</div><div class="step-check">{get_text("step1_check1", "✅ Camera, image upload, or voice note")}</div><div class="step-check">{get_text("step1_check2", "✅ Up to 5 photos in one scan")}</div><div class="step-check">{get_text("step1_check3", "✅ Works with different angles & lighting")}</div>""",
        unsafe_allow_html=True
    )

with s1_image:

    snap_food_items = [
        ("top-left", "🍅", 0),
        ("top-right", "🥦", 0.85),
        ("bottom-left", "🧀", 1.7),
        ("bottom-right", "🥕", 2.55),
    ]

    snap_item_duration = 3.4

    snap_items_html_parts = []

    for position_class, emoji, delay in snap_food_items:

        snap_items_html_parts.append(
            f'<div class="snap-item {position_class}" '
            f'style="animation-duration:{snap_item_duration}s;animation-delay:{delay}s;">{emoji}</div>'
        )

    snap_items_html = "".join(snap_items_html_parts)

    snap_status_text = get_text("snap_status_capturing", "Capturing your fridge...")

    st.markdown(
        f"""<div class="snap-wrap"><div class="snap-scanline"></div>{snap_items_html}<div class="snap-flash"></div><div class="snap-camera">📷</div><div class="ai-status-pill">📸 {snap_status_text}</div></div>""",
        unsafe_allow_html=True
    )

st.markdown(
    "<br>",
    unsafe_allow_html=True
)

s2_image, s2_text = st.columns(
    [1, 1.3]
)

with s2_image:

    orbit_emojis = ["🍅", "🫑", "🧅", "🥦", "🧄", "🥒"]
    duration = 20
    radius = 128

    orbit_html_parts = []

    for idx, emoji in enumerate(orbit_emojis):

        delay = -round(idx * (duration / len(orbit_emojis)), 2)

        orbit_html_parts.append(
            f'<div class="orbit-item" style="animation-duration:{duration}s;animation-delay:{delay}s;">'
            f'<div class="orbit-icon" style="--radius:{radius}px;animation-duration:{duration}s;animation-delay:{delay}s;">{emoji}</div>'
            f'</div>'
        )

    orbit_items_html = "".join(orbit_html_parts)

    ai_status_text = get_text("ai_status_scanning", "Scanning ingredients...")

    st.markdown(
        f"""<div class="ai-orbit-wrap"><div class="ai-orbit-scanlines"></div><div class="ai-ring r1"></div><div class="ai-ring r2"></div>{orbit_items_html}<div class="ai-core">AI</div><div class="ai-status-pill">🔎 {ai_status_text}</div></div>""",
        unsafe_allow_html=True
    )

with s2_text:

    st.markdown(
        f"""<div class="step-badge b2">{get_text("step2_badge", "Step 2")}</div><div class="step-title">{get_text("step2_title", "AI Understands Your Ingredients")}</div><div class="step-desc">{get_text("step2_desc", "Once your photos are uploaded, Gemini Vision intelligently analyzes every image and turns what it sees into a clean, organized ingredient list. Review the results, make changes, and decide exactly what goes into your recipe.")}</div><div class="step-check">{get_text("step2_check1", "✅ Smart ingredient recognition with Gemini Vision")}</div><div class="step-check">{get_text("step2_check2", "✅ Review, edit, add, or remove ingredients")}</div><div class="step-check">{get_text("step2_check3", "✅ Merges ingredients from all your photos")}</div>""",
        unsafe_allow_html=True
    )

st.markdown(
    "<br>",
    unsafe_allow_html=True
)

s3_text, s3_image = st.columns(
    [1.3, 1]
)

with s3_text:

    st.markdown(
        f"""<div class="step-badge b3">{get_text("step3_badge", "Step 3")}</div><div class="step-title">{get_text("step3_title", "Turn Ingredients Into a Feast")}</div><div class="step-desc">{get_text("step3_desc", "Let Gemini transform your available ingredients into a delicious, personalized recipe. Get everything you need to start cooking — from preparation time and servings to clear step-by-step instructions and an AI-generated preview of your finished dish.")}</div><div class="step-check">{get_text("step3_check1", "✅ Personalized recipe from your ingredients")}</div><div class="step-check">{get_text("step3_check2", "✅ Clear step-by-step cooking instructions")}</div><div class="step-check">{get_text("step3_check3", "✅ AI-generated preview of your dish")}</div>""",
        unsafe_allow_html=True
    )

with s3_image:

    steam_offsets = [-16, 0, 16]
    steam_duration = 3.2

    steam_html_parts = []

    for i, left_offset in enumerate(steam_offsets):

        delay = round(i * (steam_duration / len(steam_offsets)), 2)

        steam_html_parts.append(
            f'<div class="steam-wisp" style="left:calc(50% + {left_offset}px);'
            f'animation-duration:{steam_duration}s;animation-delay:{delay}s;"></div>'
        )

    steam_html = "".join(steam_html_parts)

    prep_badge_label = get_text("dish_badge_prep", "Prep Time")
    servings_badge_label = get_text("dish_badge_servings", "Servings")
    steps_badge_label = get_text("dish_badge_steps", "Step-by-step")
    ai_photo_badge_label = get_text("dish_badge_ai_photo", "AI-Generated Photo")

    st.markdown(
        f"""<div class="dish-wrap"><div class="dish-badge top-left" style="animation-delay:0s;"><span class="icon">⏱️</span>{prep_badge_label}</div><div class="dish-badge top-right" style="animation-delay:0.4s;"><span class="icon">👥</span>{servings_badge_label}</div><div class="dish-plate-ring"></div>{steam_html}<div class="dish-plate">🍲</div><div class="dish-badge bottom-left" style="animation-delay:0.8s;"><span class="icon">👨‍🍳</span>{steps_badge_label}</div><div class="dish-badge bottom-right" style="animation-delay:1.2s;"><span class="icon">✨</span>{ai_photo_badge_label}</div></div>""",
        unsafe_allow_html=True
    )

st.markdown(
    "<br>",
    unsafe_allow_html=True
)

footer_brand_title = get_text("footer_brand_title", "🍃 FoodRescue AI")
footer_brand_tagline = get_text(
    "footer_brand_tagline", "Turn what's left into something delicious."
)
footer_brand_desc = get_text(
    "footer_brand_desc",
    "AI-powered ingredient recognition and recipe generation "
    "designed to help you make the most of what you already "
    "have and reduce everyday food waste."
)

footer_col_product = get_text("footer_col_product", "Product")
footer_product_link1 = get_text("footer_product_link1", "How It Works")
footer_product_link2 = get_text("footer_product_link2", "Ingredient Detection")
footer_product_link3 = get_text("footer_product_link3", "Recipe Generator")
footer_product_link4 = get_text("footer_product_link4", "AI Dish Preview")

footer_col_explore = get_text("footer_col_explore", "Explore")
footer_explore_link1 = get_text("footer_explore_link1", "Features")
footer_explore_link2 = get_text("footer_explore_link2", "Multi-Photo Scanning")
footer_explore_link3 = get_text("footer_explore_link3", "Smart Ingredients")
footer_explore_link4 = get_text("footer_explore_link4", "FAQs")

footer_col_mission = get_text("footer_col_mission", "Our Mission")
footer_mission_text = get_text(
    "footer_mission_text",
    "Making everyday cooking smarter while helping households waste less food."
)
footer_highlight_bold = get_text("footer_highlight_bold", "Cook More.")
footer_highlight_sub = get_text("footer_highlight_sub", "Waste Less.")

footer_stat1_num = get_text("footer_stat1_num", "AI")
footer_stat1_label = get_text("footer_stat1_label", "Powered Recipes")
footer_stat2_num = get_text("footer_stat2_num", "5")
footer_stat2_label = get_text("footer_stat2_label", "Photos per Scan")
footer_stat3_num = get_text("footer_stat3_num", "∞")
footer_stat3_label = get_text("footer_stat3_label", "Meal Possibilities")
footer_stat4_num = get_text("footer_stat4_num", "0")
footer_stat4_label = get_text("footer_stat4_label", "Food Waste Goal")

footer_copyright = get_text(
    "footer_copyright",
    "© 2026 FoodRescue AI · Built to make every ingredient count."
)
footer_privacy = get_text("footer_privacy", "Privacy")
footer_terms = get_text("footer_terms", "Terms")
footer_contact = get_text("footer_contact", "Contact")

st.markdown(
    f"""<div class="footer-wrap"><div class="footer-top"><div class="footer-brand"><div class="footer-brand-title">{footer_brand_title}</div><div class="footer-brand-tagline">{footer_brand_tagline}</div><div class="footer-brand-desc">{footer_brand_desc}</div><div class="footer-social"><a href="#">📷</a><a href="#">💼</a><a href="#">🐙</a><a href="#">✉️</a></div></div><div class="footer-col"><div class="footer-col-title">{footer_col_product}</div><a href="#">{footer_product_link1}</a><a href="#">{footer_product_link2}</a><a href="#">{footer_product_link3}</a><a href="#">{footer_product_link4}</a></div><div class="footer-col"><div class="footer-col-title">{footer_col_explore}</div><a href="#">{footer_explore_link1}</a><a href="#">{footer_explore_link2}</a><a href="#">{footer_explore_link3}</a><a href="#">{footer_explore_link4}</a></div><div class="footer-col"><div class="footer-col-title">{footer_col_mission}</div><div class="footer-mission"><p>{footer_mission_text}</p></div><div class="footer-highlight"><strong>{footer_highlight_bold}</strong><br><span>{footer_highlight_sub}</span></div></div></div><div class="footer-divider"></div><div class="footer-stats"><div><div class="footer-stat-num">{footer_stat1_num}</div><div class="footer-stat-label">{footer_stat1_label}</div></div><div><div class="footer-stat-num">{footer_stat2_num}</div><div class="footer-stat-label">{footer_stat2_label}</div></div><div><div class="footer-stat-num">{footer_stat3_num}</div><div class="footer-stat-label">{footer_stat3_label}</div></div><div><div class="footer-stat-num">{footer_stat4_num}</div><div class="footer-stat-label">{footer_stat4_label}</div></div></div><div class="footer-bottom"><div>{footer_copyright}</div><div class="footer-bottom-links"><a href="#">{footer_privacy}</a><a href="#">{footer_terms}</a><a href="#">{footer_contact}</a></div></div></div>""",
    unsafe_allow_html=True
)
