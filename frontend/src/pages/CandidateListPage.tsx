import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Box, Typography, Paper, Tabs, Tab, Button } from '@mui/material'
import { DataGrid, GridColDef } from '@mui/x-data-grid'
import Navbar from '@/components/Navbar'
import { listCandidates } from '@/services/candidateService'

const columns: GridColDef[] = [
  { field: 'candidate_detail_id', headerName: 'ID', width: 70 },
  { field: 'candidate_name', headerName: 'Name', flex: 1 },
  { field: 'email_id', headerName: 'Email', flex: 1 },
  { field: 'overall_status', headerName: 'Status', width: 160 },
  { field: 'source', headerName: 'Source', width: 130 },
]

export default function CandidateListPage() {
  const navigate = useNavigate()
  const [candidates, setCandidates] = useState<any[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(0)

  useEffect(() => {
    listCandidates(page + 1, 20).then((data) => {
      setCandidates(data.items ?? [])
      setTotal(data.total ?? 0)
    })
  }, [page])

  return (
    <Box>
      <Navbar />
      <Box sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>Candidates</Typography>
        <Paper sx={{ height: 500 }}>
          <DataGrid
            rows={candidates}
            columns={columns}
            getRowId={(r) => r.candidate_detail_id}
            rowCount={total}
            paginationMode="server"
            paginationModel={{ page, pageSize: 20 }}
            onPaginationModelChange={(m) => setPage(m.page)}
            onRowClick={(params) => navigate(`/candidate-details/${params.row.candidate_detail_id}`)}
          />
        </Paper>
      </Box>
    </Box>
  )
}
