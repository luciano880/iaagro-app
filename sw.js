// IAAgro — Service Worker (network-first)
// Sempre tenta a versão mais recente do servidor; só cai no cache se estiver
// offline. Assim, todo deploy novo chega ao cliente no próximo acesso, sem
// deixar ninguém preso numa versão antiga (problema do cache-first anterior).

const CACHE_NAME = "iaagro-v2";

// Instala e já assume o controle sem esperar abas antigas fecharem
self.addEventListener("install", (e) => {
  self.skipWaiting();
});

// Ao ativar, apaga caches de versões anteriores e assume o controle das abas
self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((nomes) =>
      Promise.all(
        nomes.filter((n) => n !== CACHE_NAME).map((n) => caches.delete(n))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  // Só trata navegação/GET; deixa POST e outros passarem direto
  if (e.request.method !== "GET") return;

  e.respondWith(
    fetch(e.request)
      .then((resposta) => {
        // Deu certo online: atualiza o cache com a versão nova e entrega ela
        const copia = resposta.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(e.request, copia));
        return resposta;
      })
      .catch(() =>
        // Sem internet: usa o que tiver em cache (modo offline do PWA)
        caches.match(e.request).then((r) => r || Promise.reject("offline"))
      )
  );
});
