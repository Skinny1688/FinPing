# ФинПинг (FinPing) Landing Page

Рекламный лендинг для Telegram-бота финансового пульса для микробизнеса в СНГ. Сервис находится в стадии разработки — лендинг собирает лиды в лист ожидания.

## О продукте

**ФинПинг** — Telegram-бот, который помогает ИП и микробизнесу (1–5 человек) держать руку на пульсе финансов без сложных и дорогих систем учёта.

### Ключевые возможности (планируются):
- **Ежедневная сводка:** утренний пинг с доходами, расходами и остатком за предыдущий день
- **Прогноз кассового разрыва:** предупреждение о возможных проблемах с наличностью заранее
- **Автозагрузка:** интеграция с популярными банками РФ для автоматической выгрузки транзакций; ручной ввод для остальных
- **Telegram-native:** без установки отдельных приложений
- **Цена:** 500 ₽/мес (планируемая), ранний доступ бесплатно

## Интерактивный лид-магнит

Калькулятор кэшфлоу на лендинге:
- Поля: остаток, доход/расход в день, крупный платёж
- Два сценария: обычный и стресс (+20% расходов)
- График баланса по дням, персональные рекомендации
- Превью утреннего пинга, шеринг результата
- CTA: `t.me/finpingbot?start=calc`

### Запуск

Планируемый запуск — **начало июля 2026**. Первые 100 из листа ожидания — бесплатно навсегда. Тариф после запуска: 500 ₽/мес, 7 дней триала.

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
