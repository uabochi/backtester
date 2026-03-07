<template>
  <div class="trades-table">
    <div class="table-header">
      <h3>Trade History</h3>
      <div class="table-controls">
        <button @click="exportTrades" class="btn-secondary">
          📊 Export CSV
        </button>
      </div>
    </div>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th
              @click="sortBy('timestamp')"
              :class="{ active: sortField === 'timestamp' }"
            >
              Date/Time
              <span v-if="sortField === 'timestamp'" class="sort-indicator">
                {{ sortDirection === "asc" ? "↑" : "↓" }}
              </span>
            </th>
            <th
              @click="sortBy('type')"
              :class="{ active: sortField === 'type' }"
            >
              Type
              <span v-if="sortField === 'type'" class="sort-indicator">
                {{ sortDirection === "asc" ? "↑" : "↓" }}
              </span>
            </th>
            <th
              @click="sortBy('quantity')"
              :class="{ active: sortField === 'quantity' }"
            >
              Quantity
              <span v-if="sortField === 'quantity'" class="sort-indicator">
                {{ sortDirection === "asc" ? "↑" : "↓" }}
              </span>
            </th>
            <th
              @click="sortBy('price')"
              :class="{ active: sortField === 'price' }"
            >
              Price
              <span v-if="sortField === 'price'" class="sort-indicator">
                {{ sortDirection === "asc" ? "↑" : "↓" }}
              </span>
            </th>
            <th
              @click="sortBy('cash')"
              :class="{ active: sortField === 'cash' }"
            >
              Cash
              <span v-if="sortField === 'cash'" class="sort-indicator">
                {{ sortDirection === "asc" ? "↑" : "↓" }}
              </span>
            </th>
            <th
              @click="sortBy('equity')"
              :class="{ active: sortField === 'equity' }"
            >
              Equity
              <span v-if="sortField === 'equity'" class="sort-indicator">
                {{ sortDirection === "asc" ? "↑" : "↓" }}
              </span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="trade in sortedTrades"
            :key="trade.timestamp + trade.type"
            :class="trade.type.toLowerCase()"
          >
            <td>{{ formatTimestamp(trade.timestamp) }}</td>
            <td>
              <span class="trade-type" :class="trade.type.toLowerCase()">
                {{ trade.type }}
              </span>
            </td>
            <td>{{ trade.quantity }}</td>
            <td>${{ formatPrice(trade.price) }}</td>
            <td>${{ formatPrice(trade.cash) }}</td>
            <td>${{ formatPrice(trade.equity) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="trades.length === 0" class="no-trades">
      <p>No trades were executed during this backtest.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const props = defineProps({
  trades: {
    type: Array,
    default: () => [],
  },
});

const sortField = ref("timestamp");
const sortDirection = ref("desc");

const sortedTrades = computed(() => {
  if (!props.trades.length) return [];

  return [...props.trades].sort((a, b) => {
    let aVal = a[sortField.value];
    let bVal = b[sortField.value];

    // Handle string comparison
    if (typeof aVal === "string") {
      aVal = aVal.toLowerCase();
      bVal = bVal.toLowerCase();
    }

    if (sortDirection.value === "asc") {
      return aVal > bVal ? 1 : -1;
    } else {
      return aVal < bVal ? 1 : -1;
    }
  });
});

const sortBy = (field) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === "asc" ? "desc" : "asc";
  } else {
    sortField.value = field;
    sortDirection.value = "desc";
  }
};

const formatTimestamp = (timestamp) => {
  if (!timestamp) return "N/A";
  // Assuming timestamp is already in readable format
  return timestamp;
};

const formatPrice = (price) => {
  if (price === null || price === undefined) return "N/A";
  return price.toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
};

const exportTrades = () => {
  if (!props.trades.length) {
    alert("No trades to export");
    return;
  }

  // Create CSV content
  const headers = ["timestamp", "type", "quantity", "price", "cash", "equity"];
  const csvContent = [
    headers.join(","),
    ...props.trades.map((trade) =>
      headers.map((header) => trade[header] || "").join(","),
    ),
  ].join("\n");

  // Download CSV
  const blob = new Blob([csvContent], { type: "text/csv" });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "trades.csv";
  a.click();
  window.URL.revokeObjectURL(url);
};
</script>

<style scoped>
.trades-table {
  padding: 2rem;
  background: white;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.table-header h3 {
  margin: 0;
  color: #333;
  font-size: 1.2rem;
  font-weight: 600;
}

.table-controls {
  display: flex;
  gap: 0.5rem;
}

.btn-secondary {
  padding: 0.5rem 1rem;
  border: 1px solid #e1e5e9;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #f8f9fa;
}

.table-container {
  overflow-x: auto;
  border-radius: 8px;
  border: 1px solid #e1e5e9;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

thead {
  background: #f8f9fa;
}

th,
td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #e1e5e9;
}

th {
  font-weight: 600;
  color: #333;
  cursor: pointer;
  user-select: none;
  position: relative;
}

th:hover {
  background: #e9ecef;
}

th.active {
  background: #667eea;
  color: white;
}

.sort-indicator {
  margin-left: 0.25rem;
  font-size: 0.8rem;
}

tbody tr:hover {
  background: #f8f9fa;
}

.trade-type {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
}

.trade-type.buy {
  background: #d4edda;
  color: #155724;
}

.trade-type.sell {
  background: #f8d7da;
  color: #721c24;
}

.no-trades {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.no-trades p {
  margin: 0;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .trades-table {
    padding: 1rem;
  }

  .table-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .table-container {
    font-size: 0.8rem;
  }

  th,
  td {
    padding: 0.5rem;
  }
}
</style>
