-- [1] 확장 통합 ERP 시스템 초기화 스크립트
-- PostgreSQL 16+ 기준

-- UUID 확장이 필요한 경우 (PostgreSQL 버전이나 환경에 따라 선택)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. 사용자 마스터 (SaaS Isolation의 핵심)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    business_name TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. 품목 마스터 (물류 관리용)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    sku TEXT, -- 품목 코드
    current_stock INTEGER DEFAULT 0, -- 실시간 재고 수량
    base_price NUMERIC(15, 2) DEFAULT 0, -- 기본 단가
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. 계정 과목 (Chart of Accounts - 회계 관리용)
-- 초기 데이터로 '현금', '매출', '재고' 등이 사용자별로 자동 생성되어야 함
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    code TEXT NOT NULL,          -- 예: 101(현금), 146(상품재고), 401(매출액)
    name TEXT NOT NULL,          -- 계정명
    account_type TEXT NOT NULL CHECK (account_type IN ('ASSET', 'LIABILITY', 'EQUITY', 'REVENUE', 'EXPENSE')),
    UNIQUE(user_id, code)
);

-- 4. 통합 전표 마스터 (Journals / Ledger Entries)
-- 기존 ledger_entries의 개념을 확장하여 모든 거래의 '헤더' 역할을 수행
CREATE TABLE journals (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    entry_date DATE NOT NULL DEFAULT CURRENT_DATE,
    reference_no TEXT,           -- 영수증 번호 또는 외부 ID
    description TEXT,            -- 적요/메모
    product_id INTEGER REFERENCES products(id), -- 물류 연동 시 참조 (Nullable)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. 복식부기 상세 및 차대변 (Journal Items)
-- 하나의 journals(전표)는 최소 2개 이상의 items를 가짐 (차변 합 = 대변 합)
CREATE TABLE journal_items (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    journal_id INTEGER NOT NULL REFERENCES journals(id) ON DELETE CASCADE,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    
    -- 금액: 차변(debit) 또는 대변(credit)에 기록
    debit NUMERIC(15, 2) DEFAULT 0,
    credit NUMERIC(15, 2) DEFAULT 0,
    
    -- 물류 연동 수량 (필요 시 기록)
    quantity INTEGER DEFAULT 0,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- [인덱스 설정] 조회 성능 최적화
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_products_user ON products(user_id);
CREATE INDEX idx_journals_date ON journals(user_id, entry_date);
CREATE INDEX idx_items_journal ON journal_items(journal_id);