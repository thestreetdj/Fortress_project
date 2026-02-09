import React from 'react';
import { useForm } from 'react-hook-form';

export default function TransactionForm() {
    const { register, handleSubmit } = useForm();

    const onSubmit = async (data) => {
        // 백엔드 API 호출 로직 (현재 로그인된 유저의 토큰 포함)
        console.log("전송 데이터:", data);
    };

    return (
        <div className="p-6 bg-gray-50 rounded-xl shadow-sm">
            <h3 className="text-lg font-bold mb-4">02 정보입력 (매입/매출)</h3>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                <input {...register("entry_date")} type="date" className="w-full p-2 border rounded" />
                <input {...register("amount")} type="number" placeholder="금액" className="w-full p-2 border rounded" />
                <textarea {...register("memo")} placeholder="비고(거래처 등)" className="w-full p-2 border rounded" />
                <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded">저장하기</button>
            </form>
        </div>
    );
}