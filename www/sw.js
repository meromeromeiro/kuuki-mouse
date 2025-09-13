// public/sw.js
/* eslint-disable no-restricted-globals */

const CACHE_NAME = 'v1';
const urlsToCache = [
  '/', '/index.html',
];

self.addEventListener('push', event => {
  const data = event.data.json();

  event.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: 'https://avemujica.bang-dream.com/wordpress/wp-content/themes/avemujica/img/moon-r.svg',
      vibrate: [200, 100, 200]
    })
  );
});

// cache
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
      .catch(err => console.log('预缓存失败:', err))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(name => {
          if (name !== CACHE_NAME) return caches.delete(name);
          return Promise.resolve();
        })
      );
    })
  );
});

// 
self.addEventListener('install', (event) => {
  console.log("install", event)

  console.log(Notification)

  Notification.requestPermission().then(permission => {
    if (permission === "granted") {
      console.log("已获得通知权限");
    } else if (permission === "denied") {
      console.warn("用户已永久拒绝通知");
    }
  });

  const notification = new Notification("新消息提醒", {
    body: "您有3条未读消息",    // 通知正文
    icon: "/favicon.ico",         // 显示图标（推荐尺寸192x192）
    image: "/favicon.ico",     // 大图预览（部分浏览器支持）
    vibrate: [200, 100, 200],    // 振动模式（移动端）
    data: { url: "/" },   // 附加数据
    tag: "message-notify"      // 相同tag的通知会替换旧通知
  });


  // 启动每秒请求
  const timerId = setInterval(() => {
    fetch('https://moonchan.xyz')
      .then(response => {
        if (!response.ok) throw new Error(`HTTP错误: ${response.status}`);
        return response.text();
      })
      .then(data => {
        console.log(data)
      })
      .catch(error => console.error('请求失败:', error));
  }, 1000);
  setTimeout(() => { clearInterval(timerId) }, 1000 * 60)
});