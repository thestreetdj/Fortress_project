import React, { useState } from 'react';
import api from '../api/axios';

export default function JournalForm() {
  const [description, setDescription] = useState('');
  const [items, setItems] = useState([{ account_id: '', debit: 0, credit: 0 }]);

  const addRow = () => setItems([...items, { account_id: '', debit: 0, credit: 0 }]);
  
  const updateItem = (index, field, value) => {
    const newItems = [...items];
    newItems[index][field] = value;
    setItems(newItems);
  };

  const totalDebit = items.reduce((sum, i) => sum + Number(i.debit), 0);
  const totalCredit = items.reduce((sum, i) => sum + Number(i.credit), 0);

  const handleSubmit = async () => {
    if (totalDebit !== totalCredit) return alert("차대변 합계가 일치하지 않습니다.");
    try {
      await api.post('/journals/', { description, items });
      alert("전표 저장 성공!");
    } catch (err) { alert(err.response.data.detail); }
  };

  return (
    <div className="p-6 bg-white rounded shadow-md">
      <input type="text" placeholder="전표 적요" className="w-full mb-4 p-2 border" 
             onChange={e => setDescription(e.target.value)} />
      {items.map((item, idx) => (
        <div key={idx} className="flex gap-2 mb-2">
          <input placeholder="계정ID" className="border p-2 w-1/3" onChange={e => updateItem(idx, 'account_id', e.target.value)} />
          <input type="number" placeholder="차변" className="border p-2 w-1/3" onChange={e => updateItem(idx, 'debit', e.target.value)} />
          <input type="number" placeholder="대변" className="border p-2 w-1/3" onChange={e => updateItem(idx, 'credit', e.target.value)} />
        </div>
      ))}
      <button onClick={addRow} className="text-blue-500 mb-4">+ 행 추가</button>
      <div className="flex justify-between font-bold border-t pt-2">
        <span>차변 합계: {totalDebit}</span>
        <span>대변 합계: {totalCredit}</span>
      </div>
      <button onClick={handleSubmit} className="w-full mt-4 bg-green-600 text-white p-2 rounded">전표 저장</button>
    </div>
  );
}