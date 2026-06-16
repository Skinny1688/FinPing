# ФинПинг (FinPing) Landing Page

Рекламный лендинг для Telegram-бота финансового пульса для микробизнеса в СНГ. Сервис находится в стадии разработки — лендинг собирает лиды в лист ожидания.

## О продукте

**ФинПинг** — Telegram-бот, который помогает ИП и микробизнесу (1–5 человек) держать руку на пульсе финансов без сложных и дорогих систем учёта.

### Ключевые возможности (планируются):
- **Ежедневная сводка:** утренний пинг с доходами, расходами и остатком за предыдущий день
- **Прогноз кассового разрыва:** предупреждение о возможных проблемах с наличностью заранее
- **Автозагрузка:** интеграция с Т-Банк и Модульбанк (на старте)
- **Telegram-native:** без установки отдельных приложений
- **Цена:** 500 ₽/мес (планируемая), ранний доступ бесплатно

## Интерактивный лид-магнит

На лендинге встроен **калькулятор кэшфлоу** — пользователь вводит остаток, расходы и ближайший платёж, получает:
- оценку риска кассового разрыва
- превью утреннего пинга в стиле Telegram
- практические советы
- CTA в лист ожидания (`t.me/finpingbot?start=calc`)

## Технические детали

Лендинг — один статический HTML-файл (`index.html`).

- **Стек:** HTML5, CSS3 (inline), Vanilla JS
- **Дизайн:** mobile-first, палитра #0A192F / #FFFFFF / #10B981
- **Шрифты:** Inter (Google Fonts)
- **Анимации:** CSS + Intersection Observer (с поддержкой `prefers-reduced-motion`)

## Как запустить

```bash
python3 -m http.server 8000
```

Затем откройте `http://localhost:8000`.

## Telegram-бот

Бот собирает контакты потенциальных клиентов и сохраняет их в Supabase.

### Запуск

```bash
pip install aiogram supabase python-dotenv
BOT_TOKEN="your_token" SUPABASE_URL="your_url" SUPABASE_KEY="your_key" python3 bot.py
```

### Deep links

- `t.me/finpingbot` — обычный старт (`source: bot`)
- `t.me/finpingbot?start=calc` — переход с калькулятора (`source: calc`)

### Supabase

Таблица `leads`:

```sql
create table leads (
  id bigint generated always as identity primary key,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  telegram_id bigint,
  username text,
  business_info text,
  needed_functionality text,
  source text default 'bot',
  status text default 'new'
);

alter table leads enable row level security;
create policy "Allow public insert" on leads for insert with check (true);
```
