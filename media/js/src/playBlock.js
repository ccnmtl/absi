import {
    computePosition, flip, offset, shift
} from 'https://cdn.jsdelivr.net/npm/@floating-ui/dom@latest/+esm';

document.querySelectorAll('.wrapped-word').forEach((anchor) => {
    const box = document.querySelector('.float-box');

    if (!box) {
        return;
    }

    function update() {
        computePosition(anchor, box, {
            placement: 'top',
            middleware: [
                offset(6), flip(), shift()
            ],
        }).then(({ x, y }) => {
            Object.assign(box.style, {
                left: `${x}px`,
                top: `${y}px`,
            });
        });
    }


    function show() {
        box.style.display = 'block';
        update();
    }

    function hide() {
        box.style.display = 'none';
    }

    function toggle(event) {
        event.stopPropagation();

        const isOpen = box.style.display === 'block';

        document.querySelectorAll('.float-box').forEach((otherBox) => {
            otherBox.style.display = 'none';
        });

        if (!isOpen) {
            show();
        }
    }

    anchor.addEventListener('click', toggle);
    anchor.addEventListener('focus', show);
    anchor.addEventListener('blur', hide);
});

document.addEventListener('click', () => {
    document.querySelectorAll('.float-box').forEach((box) => {
        box.style.display = 'none';
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const floating = document.getElementById('floating');

    document.addEventListener('mousemove', ({ clientX, clientY }) => {
        if (!floating) return;

        Object.assign(floating.style, {
            position: 'fixed',
            left: `${clientX}px`,
            top: `${clientY}px`,
            transform: 'translate(-50%, -50%)',
            pointerEvents: 'none',
        });
    });
});
