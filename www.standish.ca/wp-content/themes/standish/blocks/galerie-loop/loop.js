(function () {

    var SLIDE_MS = 650, PAUSE_MS = 2000;
    var BIG_W = 0.40, OVERLAP = 0.20; 

    function run() {
        document.querySelectorAll('.galerie-loop-block').forEach(init);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', run);
    } else {
        run();
    }

    function init(block) {
        var stage  = block.querySelector('.galerie-loop__stage');
        var images = JSON.parse(block.dataset.images || '[]');
        var ratio = 3/4; // Portrait
        var N = images.length;
        if (!stage || N < 2) return;
        if (block.dataset.glInit) return;
        block.dataset.glInit = '1';

        var idx = 0, busy = false, timer;
        var cards = [];

        function metrics() {
            var W  = stage.offsetWidth;
            var bw = W * BIG_W;
            var bh = bw / ratio;
            var mw = bw * 0.78, mh = bh * 0.78;
            var sw = bw * 0.60, sh = bh * 0.60;
            var cy = bh / 2;
            stage.style.height = bh + 'px';

            // POSITIONS : Grande à gauche (bl), Petite à droite (sl)
            var bl = W * 0.02;
            var ml = bl + bw - (mw * OVERLAP);
            var sl = ml + mw - (sw * OVERLAP);

            return {
                slots: [
                    { w:bw, h:bh, left:bl, top:cy-bh/2, z:3, op:1 }, // Slot 0: Grosse (Gauche)
                    { w:mw, h:mh, left:ml, top:cy-mh/2, z:2, op:1 }, // Slot 1: Moyenne
                    { w:sw, h:sh, left:sl, top:cy-sh/2, z:1, op:1 }, // Slot 2: Petite (Droite)
                ],
                // On entre par la DROITE (Petite et invisible)
                offR: { w:sw, h:sh, left: W + 50, top:cy-sh/2, z:0, op:0 },
                // On sort par la GAUCHE (Grosse qui s'efface)
                exit: { w:bw, h:bh, left: -bw - 50, top:cy-bh/2, z:4, op:0 }
            };
        }

        function set(el, s, instant) {
            el.style.transition = instant ? 'none'
                : 'left ' + SLIDE_MS + 'ms cubic-bezier(.76,0,.24,1), top ' + SLIDE_MS + 'ms cubic-bezier(.76,0,.24,1), width ' + SLIDE_MS + 'ms cubic-bezier(.76,0,.24,1), height ' + SLIDE_MS + 'ms cubic-bezier(.76,0,.24,1), opacity '+ SLIDE_MS + 'ms ease';
            
            el.style.left = s.left + 'px';
            el.style.top = s.top + 'px';
            el.style.width = s.w + 'px';
            el.style.height = s.h + 'px';
            el.style.zIndex = s.z;
            el.style.opacity = s.op;

            // Important pour le CSS (scale)
            el.setAttribute('data-pos', s.z); 
        }

        function makeCard(i) {
            var d = document.createElement('div');
            d.className = 'gl-card';
            var img = document.createElement('img');
            img.src = images[(i % N + N) % N].src;
            img.alt = images[(i % N + N) % N].alt || '';
            d.appendChild(img);
            stage.appendChild(d);
            return d;
        }

        function build() {
            cards.forEach(function(c) { c.remove(); });
            cards = [];
            var m = metrics();
            // On place les 3 images de départ
            for (var i = 0; i < 3; i++) {
                var c = makeCard(idx + i);
                set(c, m.slots[i], true);
                cards.push(c);
            }
            // La carte qui attend à droite pour entrer
            var waiting = makeCard(idx + 3);
            set(waiting, m.offR, true);
            cards.push(waiting);
        }

        function slide() {
            if (busy) return;
            busy = true;
            var m = metrics();

            // LOGIQUE DE MOUVEMENT VERS LA GAUCHE
            // cards[0] (gauche) va vers EXIT
            // cards[1] (milieu) va vers GAUCHE (slots[0])
            // cards[2] (droite) va vers MILIEU (slots[1])
            // cards[3] (cachée droite) va vers DROITE (slots[2])

            set(cards[0], m.exit, false);
            set(cards[1], m.slots[0], false);
            set(cards[2], m.slots[1], false);
            set(cards[3], m.slots[2], false);

            setTimeout(function () {
                var out = cards.shift(); // On enlève celle qui est sortie à gauche
                idx = (idx + 1) % N;
                
                // On recycle l'élément pour le remettre en attente à droite
                out.querySelector('img').src = images[(idx + 3) % N].src;
                set(out, m.offR, true);
                cards.push(out);
                
                busy = false;
                timer = setTimeout(slide, PAUSE_MS);
            }, SLIDE_MS + 60);
        }

        build();
        timer = setTimeout(slide, PAUSE_MS);

        window.addEventListener('resize', function () {
            clearTimeout(timer);
            build();
            timer = setTimeout(slide, PAUSE_MS);
        });
    }
}());