import test from 'node:test';
import assert from 'node:assert/strict';
import { getRiskColor, truncate, formatCurrency, cn } from '../src/lib/utils.ts';
test('risk bands include exact decision boundaries',()=>{
 assert.equal(getRiskColor(.8),'#ff3366');assert.equal(getRiskColor(.4),'#ffaa00');assert.equal(getRiskColor(.399),'#00ff88');
});
test('formatting and class merging remain deterministic',()=>{
 assert.equal(truncate('abc',3),'abc');assert.equal(truncate('abcd',3),'abc...');assert.equal(formatCurrency(1234.5),'$1,234.50');assert.equal(cn('p-2','p-4'),'p-4');
});
