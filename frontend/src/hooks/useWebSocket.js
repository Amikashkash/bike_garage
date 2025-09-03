import { useEffect, useRef, useState } from 'react'

export function useWebSocket(url, userType = 'customer') {
  const [isConnected, setIsConnected] = useState(false)
  const [messages, setMessages] = useState([])
  const socketRef = useRef(null)
  const heartbeatRef = useRef(null)

  const connect = () => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      return
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${protocol}//${window.location.host}/ws/workshop/${userType}/`
    
    socketRef.current = new WebSocket(wsUrl)

    socketRef.current.onopen = () => {
      console.log('🔌 WebSocket connected')
      setIsConnected(true)
      startHeartbeat()
    }

    socketRef.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        console.log('📨 WebSocket message:', data)
        setMessages(prev => [...prev, data])
      } catch (error) {
        console.error('Error parsing WebSocket message:', error)
      }
    }

    socketRef.current.onclose = (event) => {
      console.log('❌ WebSocket disconnected:', event.code)
      setIsConnected(false)
      stopHeartbeat()
      
      // Auto-reconnect after 3 seconds
      setTimeout(() => {
        console.log('🔄 Attempting to reconnect...')
        connect()
      }, 3000)
    }

    socketRef.current.onerror = (error) => {
      console.error('WebSocket error:', error)
      setIsConnected(false)
    }
  }

  const startHeartbeat = () => {
    heartbeatRef.current = setInterval(() => {
      if (socketRef.current?.readyState === WebSocket.OPEN) {
        socketRef.current.send(JSON.stringify({
          type: 'ping',
          timestamp: Date.now()
        }))
      }
    }, 30000)
  }

  const stopHeartbeat = () => {
    if (heartbeatRef.current) {
      clearInterval(heartbeatRef.current)
      heartbeatRef.current = null
    }
  }

  const sendMessage = (message) => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify(message))
    } else {
      console.warn('WebSocket not connected, cannot send message')
    }
  }

  useEffect(() => {
    connect()
    
    return () => {
      stopHeartbeat()
      if (socketRef.current) {
        socketRef.current.close()
      }
    }
  }, [url, userType])

  return {
    isConnected,
    messages,
    sendMessage,
    connect
  }
}